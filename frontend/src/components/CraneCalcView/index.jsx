import React from 'react'
import { Header } from 'semantic-ui-react'

import CalculationForm from '@/src/components/CraneCalcView/CalculationForm'
import CalculationResults from '@/src/components/CraneCalcView/CalculationResults'
import useCalculationForm from '@/src/components/CraneCalcView/useCalculationForm'
import '@/src/components/CraneCalcView/CraneCalcView.css'

/**
 * Main crane calculation view component
 *
 * Provides a complete interface for calculating crane lifting capacity
 * with two calculation modes: by payload or by safety factor.
 *
 * @param {Object} crane - Crane data object containing specifications and boom lengths
 */
const CraneCalcView = ({ crane }) => {
  const {
    isChecked,
    setIsChecked,
    formData,
    errors,
    validationErrors,
    isSubmitting,
    calculationResult,
    handleInputChange,
    handleSubmit,
    handleClearForm,
  } = useCalculationForm(crane)

  return (
    <div className='calc-view-container'>
      <hr className='calc-view-divider' />
      <Header
        as='h2'
        textAlign='center'
        className='calc-view-header font-size-3'
      >
        Расcчитать грузоподъемность крана
      </Header>
      <hr className='calc-view-divider' />
      <div className='calc-input-and-result-container'>
        <CalculationForm
          crane={crane}
          formData={formData}
          errors={errors}
          validationErrors={validationErrors}
          isSubmitting={isSubmitting}
          isChecked={isChecked}
          onInputChange={handleInputChange}
          onSubmit={handleSubmit}
          onClear={handleClearForm}
          onModeChange={setIsChecked}
        />
        <CalculationResults
          calculationResult={calculationResult}
          isChecked={isChecked}
        />
      </div>
    </div>
  )
}

export default CraneCalcView
