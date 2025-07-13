import React from 'react'
import { Container, Header } from 'semantic-ui-react'

/**
 * Component to display crane calculation results
 *
 * Shows lifting capacity and either payload or safety factor based on calculation mode.
 * Displays placeholder text when no calculation has been performed.
 *
 * @param {Object} props - Component props
 * @param {Object|null} props.calculationResult - API calculation result object
 * @param {boolean} props.isChecked - Current calculation mode (determines which result to show)
 */
const CalculationResults = ({ calculationResult, isChecked }) => {
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
      <span className='calc-result-value-placeholder'>
        Выполните расчет для получения результатов
      </span>
    )
  }

  return (
    <div className='calc-result-view-container'>
      <Header as='h3' textAlign='center' className='font-size-3'>
        Результаты расчета грузоподъемности
      </Header>
      <Container className='calc-result-cards-container'>
        <div className='calc-result-card'>
          <div className='calc-result-label'>
            Грузоподъемность на данном вылете, т
          </div>
          <div className='calc-result-value font-size-4 fw-bold'>
            {calculationResult ? (
              calculationResult.base_responses[0].lifting_capacity.toFixed(2)
            ) : (
              <span className='calc-result-value-placeholder'>
                Выполните расчет для получения результатов
              </span>
            )}
          </div>
        </div>
        {isChecked ? (
          <div className='calc-result-card'>
            <div className='calc-result-label'>Допустимый вес груза, т</div>
            <div className='calc-result-value font-size-4 fw-bold'>
              {renderResultValue()}
            </div>
          </div>
        ) : (
          <>
            <div className='calc-result-card'>
              <div className='calc-result-label'>Запас грузоподъемности, т</div>
              <div className='calc-result-value font-size-4 fw-bold'>
                {calculationResult &&
                calculationResult.base_responses[0].request.payload ? (
                  calculationResult.base_responses[0].lifting_capacity -
                  calculationResult.base_responses[0].request.payload -
                  calculationResult.base_responses[0].request.equipment_weight
                ) : (
                  <span className='calc-result-value-placeholder'>
                    Выполните расчет для получения результатов
                  </span>
                )}
              </div>
            </div>

            <div className='calc-result-card'>
              <div className='calc-result-label'>Коэффициент запаса</div>
              <div className='calc-result-value font-size-4 fw-bold'>
                {renderResultValue()}
              </div>
            </div>
          </>
        )}
      </Container>
    </div>
  )
}

export default CalculationResults
