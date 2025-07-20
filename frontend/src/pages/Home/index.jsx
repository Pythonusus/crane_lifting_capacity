import React, { useEffect, useState } from 'react'

import { fetchFilteredCranes } from '@/src/api/cranes'
import CranesFilterSidebar from '@/src/components/CranesFilterSidebar'
import CranesList from '@/src/components/CranesList'
import sortCranes from '@/src/utilities/sortCranes'
import './Home.css'

/**
 * Main Home component - displays a filterable and sortable list of cranes
 * Features:
 * - Filter cranes by name, chassis type, manufacturer, and capacity range
 * - Sort cranes by various criteria
 * - Pagination for large datasets
 * - Real-time search with debouncing
 * - Responsive hidable sidebar
 */
const Home = () => {
  // State for storing the list of cranes fetched from API
  const [cranes, setCranes] = useState([])
  // Loading state to show spinner while fetching data
  const [loading, setLoading] = useState(true)
  // Error state to display error messages if API call fails
  const [error, setError] = useState(null)

  // Filter state object containing all current filter values
  const [filters, setFilters] = useState({
    model: '', // Search by crane model
    chassis_type: '', // Filter by chassis type (mobile, tower, etc.)
    manufacturer: '', // Filter by manufacturer
    min_max_lc: '', // Minimum lifting capacity filter
    max_max_lc: '', // Maximum lifting capacity filter
    sortBy: 'maxCapacityAsc', // Current sort criteria (default: capacity ascending)
  })

  /**
   * Effect hook that runs whenever filters change
   * Handles fetching, sorting, and pagination of crane data
   */
  useEffect(() => {
    // Async function to load crane data from API
    const loadCranes = async () => {
      setLoading(true) // Show loading spinner
      setError(null) // Clear any previous errors

      try {
        // Fetch filtered crane data from backend API
        const craneData = await fetchFilteredCranes(filters)

        // Apply sorting to the fetched data based on current sort criteria
        const sortedCranes = sortCranes(craneData, filters.sortBy)

        // Update state with sorted crane data
        setCranes(sortedCranes)
      } catch (error_) {
        // Handle API errors with user-friendly message
        setError('Не удалось загрузить краны. Пожалуйста, попробуйте снова.')
        console.error('Ошибка загрузки кранов:', error_)
      } finally {
        setLoading(false) // Hide loading spinner
      }
    }

    // Debounce the API call to avoid excessive requests while user is typing
    // Waits 400ms after last filter change before making API call
    const timeoutId = setTimeout(loadCranes, 400)

    // Cleanup function to cancel pending API call if filters change again
    return () => clearTimeout(timeoutId)
  }, [filters]) // Dependency array: effect runs when filters object changes

  /**
   * Handler for filter changes from the sidebar component
   * @param {Function} filterUpdater - Function that returns new filter state
   */
  const handleFiltersChange = (filterUpdater) => {
    setFilters(filterUpdater)
  }

  /**
   * Handler to reset all filters to their default values
   * Clears search terms and resets sort to default
   */
  const handleClearFilters = () => {
    setFilters({
      model: '',
      chassis_type: '',
      manufacturer: '',
      min_max_lc: '',
      max_max_lc: '',
      sortBy: 'maxCapacityAsc',
    })
  }

  return (
    <div className='home-container'>
      {/* Sidebar */}
      <aside className='home-sidebar'>
        <CranesFilterSidebar
          filters={filters}
          onFiltersChange={handleFiltersChange}
          onClearFilters={handleClearFilters}
        />
      </aside>

      {/* Main Content */}
      <main className='home-main-content'>
        <CranesList cranes={cranes} loading={loading} error={error} />
      </main>
    </div>
  )
}

export default Home
