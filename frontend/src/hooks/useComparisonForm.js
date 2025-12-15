import { useCallback, useState, useEffect } from 'react'

import {
  calculateSafetyFactor,
  createSafetyFactorRequest,
} from '@/src/api/calcRequests'
import {
  COMPARISON_TABLE_STORAGE_KEY,
  COMPARISON_FORM_STORAGE_KEY,
} from '@/src/config'
import useHistoryAdd from '@/src/hooks/useHistoryAdd'
import useHistoryState from '@/src/hooks/useHistoryState'

// Helper function to normalize numeric input (convert comma to dot for parsing)
const normalizeNumericInput = (value) => {
  if (!value) return value
  return value.replace(',', '.')
}

/**
 * Custom hook for managing comparison form state and logic
 *
 * Handles form data, validation, API calls for multiple cranes, and saving to history.
 * Provides all necessary state and handlers for the comparison form.
 *
 * @param {Array} comparisonTable - Array of comparison table entries
 * @param {Function} setComparisonTable - Function to update comparison table state
 * @returns {Object} Form state and handlers
 * @returns {Object} returns.formData - Current form field values
 * @returns {string} returns.formData.boomRadius - Boom radius value
 * @returns {string} returns.formData.equipmentWeight - Equipment weight value (optional)
 * @returns {string} returns.formData.payload - Payload value
 * @returns {Object} returns.errors - Error messages for popups
 * @returns {Object} returns.validationErrors - Validation errors for field styling
 * @returns {boolean} returns.isSubmitting - Loading state during calculation
 * @returns {Array|null} returns.comparisonResults - Array of calculation results for each crane
 * @returns {Function} returns.handleInputChange - Handler for form field changes (field: string, value: string)
 * @returns {Function} returns.handleSubmit - Handler for form submission (event: Event)
 * @returns {Function} returns.handleClearForm - Handler to reset form (no parameters)
 */
const useComparisonForm = (comparisonTable, setComparisonTable) => {
  const { history, setHistory } = useHistoryState()
  const { addToHistory } = useHistoryAdd(history, setHistory)

  // Load form data from localStorage on mount
  const [formData, setFormData] = useState(() => {
    try {
      const storedFormData = localStorage.getItem(COMPARISON_FORM_STORAGE_KEY)
      if (storedFormData) {
        const parsed = JSON.parse(storedFormData)
        return {
          boomRadius: parsed.boomRadius || '',
          equipmentWeight: parsed.equipmentWeight || '',
          payload: parsed.payload || '',
        }
      }
    } catch (error) {
      console.error('Error loading comparison form data:', error)
    }
    return {
      boomRadius: '',
      equipmentWeight: '',
      payload: '',
    }
  })

  // Save form data to localStorage whenever it changes
  useEffect(() => {
    try {
      localStorage.setItem(
        COMPARISON_FORM_STORAGE_KEY,
        JSON.stringify(formData),
      )
    } catch (error) {
      console.error('Error saving comparison form data:', error)
    }
  }, [formData])

  const [errors, setErrors] = useState({})
  const [validationErrors, setValidationErrors] = useState({})
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [comparisonResults, setComparisonResults] = useState(null)

  const handleInputChange = useCallback(
    (field, value) => {
      setFormData((prev) => ({ ...prev, [field]: value }))
      // Clear both popup and field styling when user starts typing
      // eslint-disable-next-line security/detect-object-injection
      if (errors[field]) {
        setErrors((prev) => {
          const updated = { ...prev }
          // eslint-disable-next-line security/detect-object-injection
          updated[field] = ''
          return updated
        })
      }
      // eslint-disable-next-line security/detect-object-injection
      if (validationErrors[field]) {
        setValidationErrors((prev) => {
          const updated = { ...prev }
          // eslint-disable-next-line security/detect-object-injection
          updated[field] = ''
          return updated
        })
      }
    },
    [errors, validationErrors],
  )

  const validateForm = useCallback(() => {
    const newErrors = {}
    const newValidationErrors = {}

    // Validate boom radius
    if (!formData.boomRadius || formData.boomRadius.trim() === '') {
      newErrors.boomRadius = 'Вылет стрелы обязателен для заполнения'
      newValidationErrors.boomRadius = true
    } else {
      const radius = Number.parseFloat(
        normalizeNumericInput(formData.boomRadius),
      )
      if (Number.isNaN(radius) || radius <= 0) {
        newErrors.boomRadius = 'Вылет стрелы должен быть положительным числом'
        newValidationErrors.boomRadius = true
      }
    }

    // Validate payload
    if (!formData.payload || formData.payload.trim() === '') {
      newErrors.payload = 'Вес груза обязателен для заполнения'
      newValidationErrors.payload = true
    } else {
      const payload = Number.parseFloat(normalizeNumericInput(formData.payload))
      if (Number.isNaN(payload) || payload <= 0) {
        newErrors.payload = 'Вес груза должен быть положительным числом'
        newValidationErrors.payload = true
      }
    }

    // Validate equipment weight (optional, but if provided must be valid)
    if (formData.equipmentWeight && formData.equipmentWeight.trim() !== '') {
      const equipmentWeight = Number.parseFloat(
        normalizeNumericInput(formData.equipmentWeight),
      )
      if (Number.isNaN(equipmentWeight) || equipmentWeight < 0) {
        newErrors.equipmentWeight =
          'Вес строповочного оборудования должен быть неотрицательным числом'
        newValidationErrors.equipmentWeight = true
      }
    }

    // Validate that comparison table is not empty
    if (!comparisonTable || comparisonTable.length === 0) {
      newErrors.general = 'Добавьте краны в таблицу сравнения'
    }

    setErrors(newErrors)
    setValidationErrors(newValidationErrors)

    return Object.keys(newErrors).length === 0
  }, [formData, comparisonTable])

  const handleSubmit = useCallback(
    async (e) => {
      e.preventDefault()

      if (!validateForm()) {
        return
      }

      setIsSubmitting(true)
      setComparisonResults(null)

      try {
        // Prepare all requests
        const prepareRequest = (entry) => {
          const crane = entry.crane
          const craneName = crane.name || `${crane.manufacturer}_${crane.model}`

          // Get selected boom length or default to first available
          const availableBoomLengths =
            crane.lc_tables['Основная стрела']?.boom_lengths || []
          const boomLength =
            entry.selectedBoomLength ||
            (availableBoomLengths.length > 0 ? availableBoomLengths[0] : null)

          if (!boomLength) {
            throw new Error(
              `Кран ${craneName} не имеет доступных конфигураций стрелы`,
            )
          }

          return {
            entryId: entry.id,
            crane,
            craneName,
            boomLength,
            request: createSafetyFactorRequest(
              craneName,
              boomLength,
              Number.parseFloat(normalizeNumericInput(formData.boomRadius)),
              formData.equipmentWeight
                ? Number.parseFloat(
                    normalizeNumericInput(formData.equipmentWeight),
                  )
                : 0,
              Number.parseFloat(normalizeNumericInput(formData.payload)),
            ),
          }
        }

        const requests = comparisonTable.map((entry) => prepareRequest(entry))

        // Execute all requests in parallel
        const executeCalculation = async ({
          entryId,
          crane,
          craneName,
          boomLength,
          request,
        }) => {
          try {
            const result = await calculateSafetyFactor(request)

            // Calculate remaining lifting capacity
            const remainingLc =
              result.lifting_capacity -
              request.payload -
              request.equipment_weight

            return {
              entryId,
              success: true,
              result: {
                ...result,
                remaining_lc: remainingLc,
              },
              crane,
              craneName,
              boomLength,
            }
          } catch (error) {
            console.error(`Error calculating for crane ${craneName}:`, error)
            return {
              entryId,
              success: false,
              error: error.message || 'Ошибка при выполнении расчета',
              crane,
              craneName,
              boomLength,
            }
          }
        }

        const results = await Promise.all(
          requests.map((req) => executeCalculation(req)),
        )

        // Update comparison table with results
        const findResultForEntry = (entryId, calculationResults) => {
          return calculationResults.find((r) => r.entryId === entryId)
        }

        const updateEntryWithResult = (entry, calculationResults) => {
          const result = findResultForEntry(entry.id, calculationResults)
          if (result && result.success) {
            return {
              ...entry,
              results: {
                lifting_capacity: result.result.lifting_capacity,
                safety_factor: result.result.safety_factor,
                remaining_lc: result.result.remaining_lc,
                error: null,
              },
            }
          }
          if (result && !result.success) {
            return {
              ...entry,
              results: {
                lifting_capacity: null,
                safety_factor: null,
                remaining_lc: null,
                error: 'невозможно выполнить расчет с указанным вылетом стрелы',
              },
            }
          }
          return entry
        }

        // Helper: Get entry priority (0=successful, 1=unsafe, 2=error, 3=other)
        const getEntryPriority = (entry) => {
          const hasError = !!entry.results?.error
          const safetyFactor = entry.results?.safety_factor

          if (hasError) return 2
          if (typeof safetyFactor === 'number' && safetyFactor >= 1) {
            return 0
          }
          if (typeof safetyFactor === 'number' && safetyFactor < 1) {
            return 1
          }
          return 3
        }

        const updateTableWithResults = (prevTable, calculationResults) => {
          const updatedTable = prevTable.map((entry) =>
            updateEntryWithResult(entry, calculationResults),
          )

          // Sort the table: successful (by price) -> unsafe -> errors
          const sortedTable = [...updatedTable].sort((a, b) => {
            const aPriority = getEntryPriority(a)
            const bPriority = getEntryPriority(b)

            // Compare by priority first
            if (aPriority !== bPriority) {
              return aPriority - bPriority
            }

            // Same priority: handle special cases
            if (aPriority === 0) {
              // Both successful: sort by price
              const aPrice = a.crane.price_per_hour || Infinity
              const bPrice = b.crane.price_per_hour || Infinity
              return aPrice - bPrice
            }

            // For unsafe, error, or other: keep original order
            return 0
          })

          // Save to localStorage
          localStorage.setItem(
            COMPARISON_TABLE_STORAGE_KEY,
            JSON.stringify(sortedTable),
          )

          return sortedTable
        }

        setComparisonTable((prevTable) =>
          updateTableWithResults(prevTable, results),
        )

        // Save successful calculations to history
        for (const result of results) {
          if (result.success) {
            addToHistory({
              manufacturer: result.crane.manufacturer,
              model: result.crane.model,
              country: result.crane.country || '',
              chassisType: result.crane.chassis_type || 'Unknown',
              maxLiftingCapacity:
                result.crane.max_lifting_capacity || 'Unknown',
              pricePerHour: result.crane.price_per_hour || null,
              calculationMethod: 'safety_factor',
              result: result.result,
            })
          }
        }

        // Calculate best cranes from successful results with safety factor >= 1
        const successfulResults = results.filter((r) => r.success)
        const validResults = successfulResults.filter(
          (r) =>
            r.result.safety_factor !== null &&
            r.result.safety_factor !== undefined &&
            r.result.safety_factor >= 1,
        )
        let cheapestCrane = null
        let smallestSafetyFactorCrane = null

        if (validResults.length > 0) {
          // Find cheapest crane (lowest price_per_hour)
          cheapestCrane = validResults.reduce((min, current) => {
            const minPrice = min.crane.price_per_hour || Infinity
            const currentPrice = current.crane.price_per_hour || Infinity
            return currentPrice < minPrice ? current : min
          })

          // Find crane with smallest safety factor
          smallestSafetyFactorCrane = validResults.reduce((min, current) => {
            const minSafetyFactor = min.result.safety_factor || Infinity
            const currentSafetyFactor = current.result.safety_factor || Infinity
            return currentSafetyFactor < minSafetyFactor ? current : min
          })
        }

        // Set comparison results for display with best cranes info
        setComparisonResults({
          results,
          cheapestCrane: cheapestCrane
            ? {
                name: `${cheapestCrane.crane.manufacturer} ${cheapestCrane.crane.model}`,
                boomLength: cheapestCrane.boomLength,
                price: cheapestCrane.crane.price_per_hour,
              }
            : null,
          smallestSafetyFactorCrane: smallestSafetyFactorCrane
            ? {
                name: `${smallestSafetyFactorCrane.crane.manufacturer} ${smallestSafetyFactorCrane.crane.model}`,
                boomLength: smallestSafetyFactorCrane.boomLength,
                safetyFactor: smallestSafetyFactorCrane.result.safety_factor,
              }
            : null,
        })
      } catch (error) {
        console.error('Comparison calculation error:', error)
        setErrors((prev) => ({
          ...prev,
          general: 'Ошибка при выполнении расчетов',
        }))
      } finally {
        setIsSubmitting(false)
      }
    },
    [formData, comparisonTable, setComparisonTable, validateForm, addToHistory],
  )

  const handleClearForm = useCallback(() => {
    const clearedData = {
      boomRadius: '',
      equipmentWeight: '',
      payload: '',
    }
    setFormData(clearedData)
    setErrors({})
    setValidationErrors({})
    setComparisonResults(null)
    // Clear from localStorage
    try {
      localStorage.removeItem(COMPARISON_FORM_STORAGE_KEY)
    } catch (error) {
      console.error('Error clearing comparison form data:', error)
    }
  }, [])

  return {
    formData,
    errors,
    validationErrors,
    isSubmitting,
    comparisonResults,
    handleInputChange,
    handleSubmit,
    handleClearForm,
  }
}

export default useComparisonForm
