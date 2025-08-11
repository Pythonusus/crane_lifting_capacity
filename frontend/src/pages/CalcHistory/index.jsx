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
import {
  formatCalculationValue,
  formatTimestamp,
} from '@/src/utilities/formatters'
import './CalcHistory.css'

const CalcHistory = () => {
  const { history, clearHistory } = useCalculationHistory()

  return (
    <main className='calc-history-main-content'>
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
            <Table
              celled
              striped
              compact
              size='small'
              unstackable
              className='history-table center-text'
            >
              <TableHeader>
                <TableRow>
                  <TableHeaderCell className='timestamp-column hide-on-tablet'>
                    Дата
                  </TableHeaderCell>
                  <TableHeaderCell className='crane-column'>
                    Кран
                  </TableHeaderCell>
                  <TableHeaderCell className='boom-column'>
                    Тип стрелы
                  </TableHeaderCell>
                  <TableHeaderCell className='method-column hide-on-tablet'>
                    Метод <br /> расчета
                  </TableHeaderCell>
                  <TableHeaderCell className='radius-column'>
                    Вылет
                  </TableHeaderCell>
                  <TableHeaderCell className='equipment-column'>
                    Вес <br /> оборуд.
                  </TableHeaderCell>
                  <TableHeaderCell className='input-column'>
                    <span>
                      Вес груза
                      <hr />
                      Коэф. запаса
                    </span>
                  </TableHeaderCell>
                  <TableHeaderCell className='capacity-column'>
                    Г/П <br /> на вылете
                  </TableHeaderCell>
                  <TableHeaderCell className='result-column'>
                    <span>
                      Коэф. запаса
                      <hr />
                      Вес груза
                    </span>
                  </TableHeaderCell>
                  <TableHeaderCell className='actions-column'>
                    Действия
                  </TableHeaderCell>
                </TableRow>
              </TableHeader>

              <TableBody>
                {history.map((entry) => {
                  const timestamp = formatTimestamp(entry.timestamp)

                  // Extract base response data once
                  const baseResponse = entry.result.base_responses[0]

                  const request = baseResponse.request
                  const isPayloadMethod = entry.calculationMethod === 'payload'

                  // Extract and format request values
                  const boomLength = request.boom_len
                  const radius = formatCalculationValue(request.radius, 'м')
                  const equipmentWeight = formatCalculationValue(
                    request.equipment_weight,
                    'т',
                  )

                  const inputValue = isPayloadMethod
                    ? formatCalculationValue(request.safety_factor)
                    : formatCalculationValue(request.payload, 'т')

                  // Extract and format result values
                  const liftingCapacity = formatCalculationValue(
                    baseResponse.lifting_capacity,
                    'т',
                  )

                  const calculationResult = isPayloadMethod
                    ? formatCalculationValue(baseResponse.payload, 'т')
                    : formatCalculationValue(baseResponse.safety_factor)

                  return (
                    <TableRow key={entry.id} className='table-row-hover'>
                      <TableCell className='history-timestamp hide-on-tablet'>
                        <span>
                          {timestamp.date}
                          <br />
                          {timestamp.time}
                        </span>
                      </TableCell>
                      <TableCell className='fw-bold'>
                        {entry.manufacturer} {entry.model}
                      </TableCell>
                      <TableCell>{boomLength}</TableCell>
                      <TableCell className='hide-on-tablet'>
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
                      <TableCell>{radius}</TableCell>
                      <TableCell>{equipmentWeight}</TableCell>
                      <TableCell>{inputValue}</TableCell>
                      <TableCell className='history-result-value fw-bold'>
                        {liftingCapacity}
                      </TableCell>
                      <TableCell className='history-result-value fw-bold'>
                        {calculationResult}
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
                          />
                        </div>
                      </TableCell>
                    </TableRow>
                  )
                })}
              </TableBody>
            </Table>

            <div className='history-clear-button-container'>
              <Button
                color='red'
                size='small'
                onClick={clearHistory}
                icon='trash'
                content='Очистить историю'
                className='history-clear-button'
              />
            </div>
          </>
        )}
      </div>
    </main>
  )
}

export default CalcHistory
