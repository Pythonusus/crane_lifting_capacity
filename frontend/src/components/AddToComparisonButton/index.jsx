import { useState } from 'react'
import { Button, Popup } from 'semantic-ui-react'

import { MAX_COMPARISON_TABLE_ENTRIES, POPUP_TIMEOUT } from '@/src/config'
import useComparisonTableAdd from '@/src/hooks/useComparisonTableAdd'
import useComparisonTableState from '@/src/hooks/useComparisonTableState'
import './AddToComparisonButton.css'

/**
 * Reusable button component for adding cranes to comparison table
 *
 * @param {Object} props - Component props
 * @param {string} props.craneName - Name of the crane to add (manufacturer_model format)
 * @param {string} props.className - Optional additional CSS classes
 * @param {string} props.size - Button size (default: 'small')
 * @param {boolean} props.compact - If true, shows only icon without text
 */
const AddToComparisonButton = ({
  craneName,
  className = '',
  size = 'mini',
}) => {
  const { setComparisonTable } = useComparisonTableState()
  const { addCraneToComparison } = useComparisonTableAdd(setComparisonTable)

  const [showSuccess, setShowSuccess] = useState(false)
  const [showLimitReached, setShowLimitReached] = useState(false)
  const [isLoading, setIsLoading] = useState(false)

  const handleAddToComparison = async () => {
    if (isLoading) {
      return
    }

    setIsLoading(true)
    try {
      const result = await addCraneToComparison(craneName)
      if (result.success) {
        setShowSuccess(true)
        // Hide success message after 2 seconds
        setTimeout(() => {
          setShowSuccess(false)
        }, POPUP_TIMEOUT)
      } else {
        // Handle different failure reasons
        if (result.reason === 'limit_reached') {
          setShowLimitReached(true)
          // Hide limit reached message after 2 seconds
          setTimeout(() => {
            setShowLimitReached(false)
          }, POPUP_TIMEOUT)
        }
      }
    } catch (error) {
      console.error('Error adding crane to comparison:', error)
    } finally {
      setIsLoading(false)
    }
  }

  // Determine button state and content
  let buttonContent
  let buttonIcon
  let buttonColor
  let buttonDisabled = false
  let popupContent

  if (isLoading) {
    buttonContent = ''
    buttonIcon = 'spinner'
    buttonColor = 'teal'
    buttonDisabled = true
    popupContent = 'Загрузка данных крана...'
  } else if (showSuccess) {
    buttonContent = ''
    buttonIcon = 'check'
    buttonColor = 'green'
    popupContent = 'Кран добавлен в таблицу сравнения'
  } else if (showLimitReached) {
    buttonContent = ''
    buttonIcon = 'exclamation triangle'
    buttonColor = 'orange'
    popupContent = `Достигнут лимит кранов в таблице сравнения (${MAX_COMPARISON_TABLE_ENTRIES})`
  } else {
    buttonContent = ''
    buttonIcon = 'add'
    buttonColor = 'teal'
    popupContent = 'Добавить в таблицу сравнения'
  }

  return (
    <Popup
      content={popupContent}
      size='small'
      trigger={
        <Button
          icon={buttonIcon}
          content={buttonContent}
          color={buttonColor}
          size={size}
          disabled={buttonDisabled}
          loading={isLoading}
          onClick={handleAddToComparison}
          className={`add-to-comparison-button ${className}`}
        />
      }
    />
  )
}

export default AddToComparisonButton
