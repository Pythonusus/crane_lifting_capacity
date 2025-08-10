import React, { useState } from 'react'
import { Button, Icon } from 'semantic-ui-react'

import { generateAndDownloadReport } from '@/src/utilities/reportGenerator'

/**
 * Component for downloading calculation results as a Word document
 *
 * @param {Object} props - Component props
 * @param {Object|null} props.calculationResult - API calculation result object
 * @param {boolean} props.isChecked - Current calculation mode (determines which result to show)
 * @param {Object} props.crane - Crane data object containing manufacturer and model
 * @param {Object} props.formData - Form input data
 */
const ResultDownloadButton = ({
  calculationResult,
  isChecked,
  crane,
  formData,
}) => {
  const [isGenerating, setIsGenerating] = useState(false)

  const handleDownload = async () => {
    if (!calculationResult) return

    setIsGenerating(true)
    try {
      await generateAndDownloadReport(
        calculationResult,
        isChecked,
        crane,
        formData,
      )
    } catch (error) {
      console.error('Failed to generate report:', error)
      // You could add a toast notification here if you have one
    } finally {
      setIsGenerating(false)
    }
  }

  return (
    <Button
      icon
      labelPosition='left'
      size='tiny'
      color='teal'
      onClick={handleDownload}
      disabled={!calculationResult || isGenerating}
      loading={isGenerating}
    >
      <Icon name='download' />
      {isGenerating ? 'Создание отчета...' : 'Скачать отчет DOC'}
    </Button>
  )
}

export default ResultDownloadButton
