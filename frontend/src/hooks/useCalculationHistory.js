import { useState, useEffect } from 'react'

const HISTORY_STORAGE_KEY = 'crane_calculation_history'
const MAX_HISTORY_ENTRIES = 20

/**
 * Custom hook for managing calculation history
 *
 * Stores calculation history in localStorage and provides functions to:
 * - Add new calculation results to history
 * - Retrieve all history entries
 * - Clear history
 *
 * @returns {Object} History state and functions
 * @returns {Array} returns.history - Array of calculation history entries
 * @returns {Function} returns.addToHistory - Function to add calculation to history
 * @returns {Function} returns.clearHistory - Function to clear all history
 */
const useCalculationHistory = () => {
  const [history, setHistory] = useState([])

  // Load history from localStorage on mount
  useEffect(() => {
    try {
      const storedHistory = localStorage.getItem(HISTORY_STORAGE_KEY)
      if (storedHistory) {
        const parsedHistory = JSON.parse(storedHistory)
        setHistory(parsedHistory)
      }
    } catch (error) {
      console.error('Error loading calculation history:', error)
      // Clear corrupted data
      localStorage.removeItem(HISTORY_STORAGE_KEY)
    }
  }, [])

  /**
   * Add a new calculation to history
   * @param {Object} calculation - Calculation data to store
   * @param {string} calculation.manufacturer - Manufacturer of the crane
   * @param {string} calculation.model - Model of the crane
   * @param {string} calculation.chassisType - Chassis type of the crane
   * @param {number} calculation.maxLiftingCapacity - Maximum lifting capacity of the crane
   * @param {string} calculation.boomLength - Boom length configuration
   * @param {string} calculation.calculationMethod - 'payload' or 'safety_factor'
   * @param {string} calculation.radius - Boom radius
   * @param {string} calculation.equipmentWeight - Equipment weight
   * @param {string} calculation.payload - Payload value (when calculating by safety factor)
   * @param {string} calculation.safetyFactor - Safety factor value (when calculating by payload)
   * @param {Object} calculation.result - Calculation result from API
   * @param {Date} calculation.timestamp - When the calculation was performed
   */
  const addToHistory = (calculation) => {
    try {
      const newEntry = {
        id: Date.now(), // Simple ID based on timestamp
        ...calculation,
        timestamp: new Date().toISOString(),
      }

      setHistory((prevHistory) => {
        // Add new entry to the beginning and limit to MAX_HISTORY_ENTRIES
        const updatedHistory = [newEntry, ...prevHistory].slice(
          0,
          MAX_HISTORY_ENTRIES,
        )

        // Save to localStorage
        localStorage.setItem(
          HISTORY_STORAGE_KEY,
          JSON.stringify(updatedHistory),
        )

        return updatedHistory
      })
    } catch (error) {
      console.error('Error saving calculation to history:', error)
    }
  }

  /**
   * Clear all calculation history
   */
  const clearHistory = () => {
    try {
      localStorage.removeItem(HISTORY_STORAGE_KEY)
      setHistory([])
    } catch (error) {
      console.error('Error clearing calculation history:', error)
    }
  }

  return {
    history,
    addToHistory,
    clearHistory,
  }
}

export default useCalculationHistory
