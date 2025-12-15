import React from 'react'
import { Button, Container, Header } from 'semantic-ui-react'

import { formatCalculationValue } from '@/src/utilities/formatters'
import './ComparisonResult.css'

/**
 * Component to display comparison calculation results
 *
 * Shows results for multiple cranes in a card-based format similar to CalculationResults.
 * Displays lifting capacity, safety factor/payload, and remaining capacity for each crane.
 *
 * @param {Object} props - Component props
 * @param {Array} props.comparisonResults - Array of comparison results with crane and results data
 * @param {string} props.calculationMode - Calculation mode ('payload' or 'safety_factor')
 */
const ComparisonResult = ({ comparisonResults }) => {
  const renderCheapestCrane = () => {
    if (!comparisonResults) {
      return (
        <span className='comparison-result-value-placeholder'>
          Выполните расчет для получения результатов
        </span>
      )
    }

    if (comparisonResults.cheapestCrane) {
      const { name, boomLength, price } = comparisonResults.cheapestCrane
      const displayName = boomLength ? `${name} (${boomLength})` : name
      if (price !== null && price !== undefined) {
        return (
          <>
            {displayName} -{' '}
            <span className='comparison-result-value-green'>
              {formatCalculationValue(price)} ₽
            </span>
          </>
        )
      }
      return displayName
    }

    return (
      <span className='comparison-result-no-crane-message'>
        Ни один кран не подошел
      </span>
    )
  }

  const renderSmallestSafetyFactorCrane = () => {
    if (!comparisonResults) {
      return (
        <span className='comparison-result-value-placeholder'>
          Выполните расчет для получения результатов
        </span>
      )
    }

    if (comparisonResults.smallestSafetyFactorCrane) {
      const { name, boomLength, safetyFactor } =
        comparisonResults.smallestSafetyFactorCrane
      const displayName = boomLength ? `${name} (${boomLength})` : name
      if (safetyFactor !== null && safetyFactor !== undefined) {
        return (
          <>
            {displayName} -{' '}
            <span className='comparison-result-value-green'>
              {formatCalculationValue(safetyFactor)}
            </span>
          </>
        )
      }
      return displayName
    }

    return (
      <span className='comparison-result-no-crane-message'>
        Ни один кран не подошел
      </span>
    )
  }

  return (
    <div className='comparison-results'>
      <Header
        as='h3'
        textAlign='center'
        className='comparison-results-header font-size-4'
      >
        Результаты сравнения
      </Header>
      <Container className='comparison-results-cards-container'>
        <div className='comparison-results-card'>
          <div className='comparison-results-label font-size-5 fw-bold'>
            Наименьшая стоимость маш.-ч
          </div>
          <div className='comparison-results-value font-size-5 fw-bold'>
            {renderCheapestCrane()}
          </div>
        </div>
        <div className='comparison-results-card'>
          <div className='comparison-results-label font-size-5 fw-bold'>
            Наименьший коэффициент запаса
          </div>
          <div className='comparison-results-value font-size-5 fw-bold'>
            {renderSmallestSafetyFactorCrane()}
          </div>
        </div>
        <div className='comparison-results-actions'>
          <Button
            icon
            labelPosition='left'
            size='tiny'
            color='teal'
            fluid
            disabled={!comparisonResults || !comparisonResults.results}
            className='comparison-results-copy-button'
          >
            Копировать результат
          </Button>

          <Button
            icon
            labelPosition='left'
            size='tiny'
            color='teal'
            fluid
            disabled={!comparisonResults || !comparisonResults.results}
            className='comparison-results-download-button'
          >
            Скачать отчет DOC
          </Button>
        </div>
      </Container>
    </div>
  )
}

export default ComparisonResult
