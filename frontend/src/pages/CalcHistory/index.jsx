import React from 'react'
import {
  Button,
  Header,
  Message,
  Table,
  TableBody,
  TableCell,
  TableHeader,
  TableHeaderCell,
  TableRow,
} from 'semantic-ui-react'

import ResultCopyButton from '@/src/components/CraneCalcView/ResultCopyButton'
import ResultDownloadButton from '@/src/components/CraneCalcView/ResultDownloadButton'
import useCalculationHistory from '@/src/hooks/useCalculationHistory'
import './CalcHistory.css'

const formatTimestamp = (timestamp) => {
  const date = new Date(timestamp)
  const dateStr = date.toLocaleDateString('ru-RU', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
  })
  const timeStr = date.toLocaleTimeString('ru-RU', {
    hour: '2-digit',
    minute: '2-digit',
  })
  return (
    <span>
      {dateStr}
      <br />
      {timeStr}
    </span>
  )
}

const getResultValue = (entry) => {
  if (
    !entry.result ||
    !entry.result.base_responses ||
    !entry.result.base_responses[0]
  ) {
    return 'N/A'
  }

  const baseResponse = entry.result.base_responses[0]

  // Extract the calculated result based on calculation method
  if (entry.calculationMethod === 'payload') {
    // For payload calculations, show the calculated payload
    return baseResponse.payload ? `${baseResponse.payload.toFixed(2)} т` : 'N/A'
  } else {
    // For safety factor calculations, show the calculated safety factor
    return baseResponse.safety_factor
      ? baseResponse.safety_factor.toFixed(2)
      : 'N/A'
  }
}

const getLiftingCapacity = (entry) => {
  if (
    !entry.result ||
    !entry.result.base_responses ||
    !entry.result.base_responses[0]
  ) {
    return 'N/A'
  }

  const baseResponse = entry.result.base_responses[0]

  // Extract lifting capacity at the given radius from the result
  return baseResponse.lifting_capacity
    ? `${baseResponse.lifting_capacity.toFixed(2)} т`
    : 'N/A'
}

const getComplementaryValue = (entry) => {
  // Return the input value that wasn't calculated
  if (entry.calculationMethod === 'payload') {
    return entry.safetyFactor || 'N/A'
  } else {
    return entry.payload ? `${entry.payload} т` : 'N/A'
  }
}

const reconstructFormData = (entry) => {
  return {
    boomLength: entry.boomLength,
    boomRadius: entry.radius,
    equipmentWeight: entry.equipmentWeight,
    payload: entry.payload,
    safetyFactor: entry.safetyFactor,
  }
}

const CalcHistory = () => {
  const { history, clearHistory } = useCalculationHistory()

  return (
    <div className='calc-history-container'>
      <Header as='h1' textAlign='center' className='font-size-2'>
        История расчетов
      </Header>

      {history.length === 0 ? (
        <Message info>
          <Message.Header>История пуста</Message.Header>
          <p>Выполните расчеты, чтобы увидеть их здесь.</p>
        </Message>
      ) : (
        <>
          <Table celled striped compact unstackable className='history-table'>
            <TableHeader>
              <TableRow>
                <TableHeaderCell className='timestamp-column'>
                  Дата
                </TableHeaderCell>
                <TableHeaderCell className='crane-column'>Кран</TableHeaderCell>
                <TableHeaderCell className='boom-column'>
                  Тип стрелы
                </TableHeaderCell>
                <TableHeaderCell className='method-column'>
                  Метод расчета
                </TableHeaderCell>
                <TableHeaderCell className='radius-column'>
                  Вылет (м)
                </TableHeaderCell>
                <TableHeaderCell className='equipment-column hide-on-tablet'>
                  Вес оборуд. (т)
                </TableHeaderCell>
                <TableHeaderCell className='input-column'>
                  <span>
                    Вес груза (т) /
                    <br />
                    Коэф. запаса
                  </span>
                </TableHeaderCell>
                <TableHeaderCell className='capacity-column'>
                  Г/П на вылете (т)
                </TableHeaderCell>
                <TableHeaderCell className='result-column'>
                  Результат расчета
                </TableHeaderCell>
                <TableHeaderCell className='actions-column'>
                  Действия
                </TableHeaderCell>
              </TableRow>
            </TableHeader>

            <TableBody>
              {history.map((entry) => (
                <TableRow key={entry.id} className='table-row-hover'>
                  <TableCell className='history-timestamp center-content'>
                    {formatTimestamp(entry.timestamp)}
                  </TableCell>
                  <TableCell className='history-crane-name'>
                    {entry.manufacturer} {entry.model}
                  </TableCell>
                  <TableCell>{entry.boomLength}</TableCell>
                  <TableCell>
                    {entry.calculationMethod === 'payload' ? (
                      <span className='history-method-label font-size-5'>
                        Коэф. запаса
                      </span>
                    ) : (
                      <span className='history-method-label font-size-5'>
                        Вес груза
                      </span>
                    )}
                  </TableCell>
                  <TableCell>{entry.radius}</TableCell>
                  <TableCell className='hide-on-tablet'>
                    {entry.equipmentWeight || '0'}
                  </TableCell>
                  <TableCell>{getComplementaryValue(entry)}</TableCell>
                  <TableCell className='history-result-value'>
                    {getLiftingCapacity(entry)}
                  </TableCell>
                  <TableCell className='history-result-value'>
                    {getResultValue(entry)}
                  </TableCell>
                  <TableCell>
                    <div className='history-action-buttons'>
                      <ResultCopyButton
                        calculationResult={entry.result}
                        isChecked={entry.calculationMethod === 'payload'}
                        crane={{
                          name: `${entry.manufacturer}_${entry.model}`,
                          manufacturer: entry.manufacturer,
                          model: entry.model,
                          chassis_type: entry.chassisType || null,
                          max_lifting_capacity:
                            entry.maxLiftingCapacity || null,
                        }}
                      />
                      <ResultDownloadButton
                        calculationResult={entry.result}
                        isChecked={entry.calculationMethod === 'payload'}
                        crane={{
                          name: `${entry.manufacturer}_${entry.model}`,
                          manufacturer: entry.manufacturer,
                          model: entry.model,
                          chassis_type: entry.chassisType || null,
                          max_lifting_capacity:
                            entry.maxLiftingCapacity || null,
                        }}
                        formData={reconstructFormData(entry)}
                      />
                    </div>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>

          <div
            style={{ textAlign: 'right', marginTop: '1rem' }}
            className='history-clear-button'
          >
            <Button
              color='red'
              size='small'
              onClick={clearHistory}
              icon='trash'
              content='Очистить историю'
            />
          </div>
        </>
      )}
    </div>
  )
}

export default CalcHistory
