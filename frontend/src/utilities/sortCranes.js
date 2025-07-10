/**
 * Utility function to sort crane data based on different criteria
 * @param {Array} cranes - Array of crane objects to sort
 * @param {string} sortBy - Sort criteria identifier
 * @returns {Array} Sorted array of cranes
 */
const sortCranes = (cranes, sortBy) => {
  // Create a shallow copy to avoid mutating the original array
  const sortedCranes = [...cranes]

  switch (sortBy) {
    // Sort by maximum lifting capacity in ascending order (lowest to highest)
    case 'maxCapacityAsc': {
      return sortedCranes.sort(
        (a, b) => a.max_lifting_capacity - b.max_lifting_capacity,
      )
    }
    // Sort by maximum lifting capacity in descending order (highest to lowest)
    case 'maxCapacityDesc': {
      return sortedCranes.sort(
        (a, b) => b.max_lifting_capacity - a.max_lifting_capacity,
      )
    }
    // Sort by manufacturer + model name in ascending order (A-Z)
    case 'displayNameAsc': {
      return sortedCranes.sort((a, b) => {
        const displayNameA = `${a.manufacturer} ${a.model}`
        const displayNameB = `${b.manufacturer} ${b.model}`
        return displayNameA.localeCompare(displayNameB)
      })
    }
    // Sort by manufacturer + model name in descending order (Z-A)
    case 'displayNameDesc': {
      return sortedCranes.sort((a, b) => {
        const displayNameA = `${a.manufacturer} ${a.model}`
        const displayNameB = `${b.manufacturer} ${b.model}`
        return displayNameB.localeCompare(displayNameA)
      })
    }
    // Sort by price per hour in ascending order (cheapest first)
    case 'pricePerHourAsc': {
      return sortedCranes.sort((a, b) => {
        const priceA = (a.base_price || 0) + (a.labor_cost || 0)
        const priceB = (b.base_price || 0) + (b.labor_cost || 0)
        return priceA - priceB
      })
    }
    // Sort by price per hour in descending order (most expensive first)
    case 'pricePerHourDesc': {
      return sortedCranes.sort((a, b) => {
        const priceA = (a.base_price || 0) + (a.labor_cost || 0)
        const priceB = (b.base_price || 0) + (b.labor_cost || 0)
        return priceB - priceA
      })
    }
    // Default case: return unsorted array
    default: {
      return sortedCranes
    }
  }
}

export default sortCranes
