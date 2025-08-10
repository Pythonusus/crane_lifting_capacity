import React from 'react'
import { Container, Header } from 'semantic-ui-react'

import ResultCopyButton from './ResultCopyButton'

/**
 * Component to display crane calculation results
 *
 * Shows lifting capacity and either payload or safety factor based on calculation mode.
 * Displays placeholder text when no calculation has been performed.
 *
 * @param {Object} props - Component props
 * @param {Object|null} props.calculationResult - API calculation result object
 * @param {boolean} props.isChecked - Current calculation mode (determines which result to show)
 * @param {Object} props.crane - Crane data object containing manufacturer and model
 */
const CalculationResults = ({ calculationResult, isChecked, crane }) => {
  const renderResultValue = () => {
    if (!calculationResult) {
      return (
        <span className='calc-result-value-placeholder'>
          Выполните расчет для получения результатов
        </span>
      )
    }

    const baseResponse = calculationResult.base_responses[0]

    if (isChecked) {
      // When calculating by safety factor, show payload
      if (baseResponse.payload) {
        return baseResponse.payload.toFixed(2)
      }
      return (
        <span className='calc-result-value-placeholder'>
          Выполните расчет для получения результатов
        </span>
      )
    }

    // When calculating by payload, show safety factor
    if (baseResponse.safety_factor) {
      return baseResponse.safety_factor.toFixed(2)
    }
    return (
      <span className='calc-result-value-placeholder font-size-5'>
        Выполните расчет для получения результатов
      </span>
    )
  }

  return (
    <div className='calc-result-view-container'>
      <Header as='h3' textAlign='center' className='font-size-4'>
        Результаты расчета грузоподъемности
      </Header>
      <Container className='calc-result-cards-container'>
        <div className='calc-result-card'>
          <div className='calc-result-label font-size-5 fw-bold'>
            Грузоподъемность на данном вылете, т
          </div>
          <div className='calc-result-value font-size-5 fw-bold'>
            {calculationResult ? (
              calculationResult.base_responses[0].lifting_capacity.toFixed(2)
            ) : (
              <span className='calc-result-value-placeholder font-size-5'>
                Выполните расчет для получения результатов
              </span>
            )}
          </div>
        </div>
        {isChecked ? (
          <div className='calc-result-card'>
            <div className='calc-result-label font-size-5 fw-bold'>
              Допустимый вес груза, т
            </div>
            <div className='calc-result-value font-size-5 fw-bold'>
              {renderResultValue()}
            </div>
          </div>
        ) : (
          <>
            <div className='calc-result-card'>
              <div className='calc-result-label font-size-5 fw-bold'>
                Коэффициент запаса
              </div>
              <div className='calc-result-value font-size-5 fw-bold'>
                {renderResultValue()}
              </div>
            </div>
            <div className='calc-result-card'>
              <div className='calc-result-label font-size-5 fw-bold'>
                Запас грузоподъемности, т
              </div>
              <div className='calc-result-value font-size-5 fw-bold'>
                {calculationResult &&
                calculationResult.base_responses[0].request.payload ? (
                  (
                    calculationResult.base_responses[0].lifting_capacity -
                    calculationResult.base_responses[0].request.payload -
                    calculationResult.base_responses[0].request.equipment_weight
                  ).toFixed(2)
                ) : (
                  <span className='calc-result-value-placeholder font-size-5'>
                    Выполните расчет для получения результатов
                  </span>
                )}
              </div>
            </div>
          </>
        )}
        <ResultCopyButton
          calculationResult={calculationResult}
          isChecked={isChecked}
          crane={crane}
        />
      </Container>
    </div>
  )
}

export default CalculationResults
