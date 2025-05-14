import { render, screen } from '@testing-library/react'

import App from '../src/App.jsx'

describe('App Component', () => {
  test('renders without crashing', () => {
    render(<App />)
    // You can add more specific assertions here
    expect(screen.getByRole('heading')).toBeInTheDocument()
  })
})
