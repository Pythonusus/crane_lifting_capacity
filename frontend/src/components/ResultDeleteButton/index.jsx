import { Button, Icon } from 'semantic-ui-react'

import './ResultDeleteButton.css'

/**
 * Component for deleting a calculation result
 *
 * @param {Object} props - Component props
 * @param {Function} props.deleteSingleEntry - Function to delete the calculation result
 * @param {number} props.entryId - ID of the calculation result to delete
 */
const ResultDeleteButton = ({ deleteSingleEntry, entryId }) => {
  const handleDelete = () => {
    if (
      globalThis.confirm(
        'Вы уверены, что хотите удалить этот расчет из истории? Это действие нельзя отменить.',
      )
    ) {
      deleteSingleEntry(entryId)
    }
  }

  return (
    <Button
      icon
      labelPosition='left'
      color='red'
      size='tiny'
      fluid
      onClick={handleDelete}
      className='result-delete-button'
    >
      <Icon name='trash' />
      Удалить расчет
    </Button>
  )
}

export default ResultDeleteButton
