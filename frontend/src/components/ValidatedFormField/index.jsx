import React from 'react'
import { FormField, Popup } from 'semantic-ui-react'

/**
 * Reusable form field component with validation display
 *
 * Provides consistent validation styling and error popups for form fields.
 * Supports both regular inputs and custom components like dropdowns.
 *
 * @param {Object} props - Component props
 * @param {string} props.field - Field name for ID generation
 * @param {string} props.label - Field label text
 * @param {string} [props.placeholder] - Input placeholder text
 * @param {string} props.value - Current field value
 * @param {Function} props.onChange - Handler for value changes (receives string value)
 * @param {string} [props.error] - Error message for popup display
 * @param {string} [props.validationError] - Error state for field styling
 * @param {React.ReactNode} [props.children] - Custom component (like dropdown)
 * @param {string} [props.type='input'] - Field type ('input' or 'dropdown')
 */
const ValidatedFormField = ({
  field,
  label,
  placeholder,
  value,
  onChange,
  error,
  validationError,
  children,
  type = 'input',
}) => {
  const renderField = () => {
    if (children) {
      return children
    }

    if (type === 'dropdown') {
      return value
    }

    return (
      <input
        placeholder={placeholder}
        value={value}
        onChange={(e) => onChange(e.target.value)}
      />
    )
  }

  return (
    <FormField error={!!validationError} className='mb-5'>
      <label htmlFor={`${field}-${type}`}>
        {label}
        <Popup
          content={error}
          open={!!error}
          position='left center'
          color='red'
          size='small'
          onClose={() => onChange(value)}
          trigger={renderField()}
        />
      </label>
    </FormField>
  )
}

export default ValidatedFormField
