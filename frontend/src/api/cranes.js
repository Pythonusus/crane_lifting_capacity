/**
 * Fetches filtered cranes from the backend
 * @param {Object} [filters={}] - Criteria to filter cranes
 * @returns {Promise<Array>} List of cranes matching the filters
 *
 * @example
 * Get all cranes (no filters)
 * fetchFilteredCranes()
 *
 * Filter by chassis type
 * fetchFilteredCranes({ chassisType: 'mobile' })
 *
 * Filter by multiple criteria
 * fetchFilteredCranes({
 *   chassisType: 'mobile',
 *   manufacturer: 'Liebherr',
 *   resourceCode: 'ABC123',
 * })
 */
export const fetchFilteredCranes = async (filters = {}) => {
  const response = await fetch('/cranes/filter', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ filters }),
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
  const response = await fetch('/chassis-types')

  if (!response.ok) {
    throw new Error('Failed to fetch chassis types')
  }

  const data = await response.json()
  return data.chassisTypes || []
}
