import React from 'react'
import { Header, Table } from 'semantic-ui-react'

import ImageGallery from '@/src/components/ImageGallery'
import './CraneDataView.css'

const CraneView = ({ crane }) => {
  const getLcTableRows = (lc_table) => {
    const boomLengths = crane.lc_table_boom_lengths
    const radiuses = crane.lc_table_radiuses
    const rows = []
    for (const radius of radiuses) {
      const row = [radius]
      for (const boomLength of boomLengths) {
        // boomLength and radius are not user-controlled, so we can use them as keys
        // eslint-disable-next-line security/detect-object-injection
        const capacity = lc_table[boomLength]?.[radius] || '-'
        row.push(capacity)
      }
      rows.push(row)
    }
    return rows
  }

  const lcTableRows = getLcTableRows(crane.lc_table)

  return (
    <div className='crane-data-view-container'>
      <div className='crane-metadata-container'>
        <Table compact celled striped unstackable size='small'>
          <Table.Header>
            <Table.Row>
              <Table.HeaderCell colSpan='2' className='table-main-header'>
                <Header as='h2' textAlign='center' className='font-size-3'>
                  Характеристики крана
                </Header>
              </Table.HeaderCell>
            </Table.Row>
          </Table.Header>
          <Table.Body>
            <Table.Row>
              <Table.Cell>
                <b>Тип шасси:</b>
              </Table.Cell>
              <Table.Cell>{crane.chassis_type}</Table.Cell>
            </Table.Row>
            <Table.Row>
              <Table.Cell>
                <b>Макс. грузоподъемность:</b>
              </Table.Cell>
              <Table.Cell>{crane.max_lifting_capacity}т</Table.Cell>
            </Table.Row>
            <Table.Row>
              <Table.Cell>
                <b>Код по {crane.pricebook}:</b>
              </Table.Cell>
              <Table.Cell>{crane.resource_code}</Table.Cell>
            </Table.Row>
            <Table.Row>
              <Table.Cell>
                <b>Базовая цена:</b>
              </Table.Cell>
              <Table.Cell>{crane.base_price} руб./маш.-ч</Table.Cell>
            </Table.Row>
            <Table.Row>
              <Table.Cell>
                <b>Зарплата машиниста:</b>
              </Table.Cell>
              <Table.Cell>{crane.labor_cost} руб./маш.-ч</Table.Cell>
            </Table.Row>
            <Table.Row>
              <Table.Cell>
                <b>Cуммарная стоимость:</b>
              </Table.Cell>
              <Table.Cell>{crane.price_per_hour} руб./маш.-ч</Table.Cell>
            </Table.Row>
            <Table.Row>
              <Table.Cell textAlign='top'>
                <b>Доступные загрузки:</b>
              </Table.Cell>
              <Table.Cell>
                <div className='attachments-container'>
                  {crane.attachments
                    .filter((attachment) => !attachment.is_inline)
                    .map((attachment) => (
                      <div key={attachment.id} className='attachment-item'>
                        <a
                          href={`/api/attachments/${attachment.id}`}
                          className='attachment-link'
                          target='_blank'
                          rel='noopener noreferrer'
                        >
                          <i className='file icon'></i>
                          {attachment.filename}
                        </a>
                      </div>
                    ))}
                </div>
              </Table.Cell>
            </Table.Row>
          </Table.Body>
        </Table>
        <ImageGallery attachments={crane.attachments} />
      </div>

      <div className='table-scrollable-container'>
        <Table
          compact
          celled
          striped
          size='small'
          unstackable
          className='custom-small-table'
        >
          <Table.Header className='sticky-top'>
            <Table.Row>
              <Table.HeaderCell
                colSpan={crane.lc_table_boom_lengths.length + 1}
                className='table-main-header'
              >
                <Header as='h2' textAlign='center' className='font-size-3'>
                  Таблица грузоподъемности (т)
                </Header>
              </Table.HeaderCell>
            </Table.Row>
            <Table.Row>
              <Table.HeaderCell className='sticky-left'></Table.HeaderCell>
              <Table.HeaderCell
                colSpan={crane.lc_table_boom_lengths.length}
                textAlign='center'
                className='font-size-4'
              >
                Конфигурация стрелы
              </Table.HeaderCell>
            </Table.Row>
            <Table.Row textAlign='center'>
              <Table.HeaderCell className='sticky-left'>
                Вылет, м
              </Table.HeaderCell>
              {crane.lc_table_boom_lengths.map((boomLength) => (
                <Table.HeaderCell key={boomLength}>
                  {boomLength}
                </Table.HeaderCell>
              ))}
            </Table.Row>
          </Table.Header>
          <Table.Body>
            {lcTableRows.map((row, index) => (
              <Table.Row key={index} className='lc_table_body_row'>
                {row.map((cell, cellIndex) => (
                  <Table.Cell key={cellIndex}>{cell}</Table.Cell>
                ))}
              </Table.Row>
            ))}
          </Table.Body>
        </Table>
      </div>
    </div>
  )
}

export default CraneView
