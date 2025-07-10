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
 *   name: 'LR1100',
 *   chassis_type: 'mobile',
 *   manufacturer: 'Liebherr',
 *   min_max_lc: 100,
 *   max_max_lc: 500,
 * })
 */
export const fetchFilteredCranes = async (filters = {}) => {
  // Clean up filters: convert empty strings to null and remove sortBy
  const cleanedFilters = {
    name:
      filters.name === '' || filters.name === null || filters.name === undefined
        ? null
        : filters.name,
    manufacturer:
      filters.manufacturer === '' ||
      filters.manufacturer === null ||
      filters.manufacturer === undefined
        ? null
        : filters.manufacturer,
    chassis_type:
      filters.chassis_type === '' ||
      filters.chassis_type === null ||
      filters.chassis_type === undefined
        ? null
        : filters.chassis_type,
    min_max_lc:
      filters.min_max_lc === '' ||
      filters.min_max_lc === null ||
      filters.min_max_lc === undefined
        ? null
        : filters.min_max_lc,
    max_max_lc:
      filters.max_max_lc === '' ||
      filters.max_max_lc === null ||
      filters.max_max_lc === undefined
        ? null
        : filters.max_max_lc,
  }

  const response = await fetch('/cranes', {
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
  const response = await fetch('/chassis-types')

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
  const response = await fetch('/manufacturers')

  if (!response.ok) {
    throw new Error('Failed to fetch manufacturers')
  }

  const data = await response.json()
  return data.manufacturers || []
}
