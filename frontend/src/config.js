/**
 * Pagination configuration for the application
 *
 * Default number of items to load per page/batch
 * Used for initial load and "Show More" functionality
 */
export const PAGINATION_SIZE = Number.parseInt(
  import.meta.env.PAGINATION_SIZE || '15',
  10,
)
