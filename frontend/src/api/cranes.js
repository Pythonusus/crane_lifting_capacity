/**
 * API requests for fetching cranes and related data
 * @module api/cranes
 */

import { formatFormValue } from '@/src/utilities/formatters'

/**
 * Fetches filtered cranes from the backend
 * @param {Object} [filters={}] - Criteria to filter cranes
 * @returns {Promise<Array>} List of cranes matching the filters
 *
 * @example
 * Get all cranes (no filters)
 * fetchFilteredCranes()
 *
 * Filter by single criteria
 * fetchFilteredCranes({ chassis_type: 'mobile' })
 *
 * Filter by multiple criteria
 * fetchFilteredCranes({
 *   model: 'LR1100',
 *   chassis_type: 'mobile',
 *   manufacturer: 'Liebherr',
 *   min_max_lc: 100,
 *   max_max_lc: 500,
 * })
 */
export const fetchFilteredCranes = async (filters = {}) => {
  // Clean up filters: convert empty strings to null and remove sortBy
  const cleanedFilters = {
    model: formatFormValue(filters.model),
    manufacturer: formatFormValue(filters.manufacturer),
    chassis_type: formatFormValue(filters.chassis_type),
    min_max_lc: formatFormValue(filters.min_max_lc),
    max_max_lc: formatFormValue(filters.max_max_lc),
  }

  const response = await fetch('/api/cranes', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(cleanedFilters),
  })

  if (!response.ok) {
    throw new Error('Failed to fetch cranes')
  }

  const data = await response.json()
  return data.cranes || []
}

/**
 * Fetches all available chassis types from the backend
 * @returns {Promise<string[]>} List of available chassis types
 */
export const fetchChassisTypes = async () => {
  const response = await fetch('/api/chassis-types')

  if (!response.ok) {
    throw new Error('Failed to fetch chassis types')
  }

  const data = await response.json()
  return data.chassisTypes || []
}

/**
 * Fetches all available manufacturers from the backend
 * @returns {Promise<string[]>} List of available manufacturers
 */
export const fetchManufacturers = async () => {
  const response = await fetch('/api/manufacturers')

  if (!response.ok) {
    throw new Error('Failed to fetch manufacturers')
  }

  const data = await response.json()
  return data.manufacturers || []
}

/**
 * Fetches a single crane by name from the backend
 * @param {string} craneName - Name of the crane to fetch (format: "Manufacturer Model")
 * @returns {Promise<Object>} The crane object
 */
export const fetchCraneByName = async (craneName) => {
  const response = await fetch(`/api/cranes/${encodeURIComponent(craneName)}`)

  if (!response.ok) {
    if (response.status === 404) {
      throw new Error('Crane not found')
    }
    throw new Error('Failed to fetch crane')
  }

  return await response.json()
}
