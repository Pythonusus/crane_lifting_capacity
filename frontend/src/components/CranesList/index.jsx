import React from 'react'
import { Link } from 'react-router-dom'
import {
  Container,
  Header,
  Icon,
  Message,
  Popup,
  Table,
  TableBody,
  TableCell,
  TableHeader,
  TableHeaderCell,
  TableRow,
} from 'semantic-ui-react'
import './CranesList.css'

const CranesList = ({ cranes = [], loading = false, error = null }) => {
  if (loading && cranes.length === 0) {
    return (
      <Container>
        <div className='loading-container'>
          <Icon name='spinner' loading size='huge' />
          <Header as='h2' className='loading-header'>
            Загружаем краны...
          </Header>
        </div>
      </Container>
    )
  }

  return (
    <>
      <Header as='h1' className='main-header m-top center-content'>
        <Icon name='cogs' />
        <Header.Content className='resize-text-on-tablet'>
          Доступные краны
          <Header.Subheader>Всего найдено: {cranes.length}</Header.Subheader>
        </Header.Content>
      </Header>

      {/* Error Message */}
      {error && (
        <Message negative>
          <Message.Header>Ошибка</Message.Header>
          <p>{error}</p>
        </Message>
      )}

      {/* Show cranes if available */}
      {cranes.length > 0 ? (
        <Table celled striped compact unstackable>
          <TableHeader className='cranes-table-header'>
            <TableRow>
              <TableHeaderCell>Название</TableHeaderCell>
              <TableHeaderCell>Тип шасси</TableHeaderCell>
              <TableHeaderCell className='hide-on-tablet'>
                Код ресурса по ФСЭМ-2022
              </TableHeaderCell>
              <TableHeaderCell className='hide-on-tablet'>
                Стоимость маш.-ч (₽)
              </TableHeaderCell>
              <TableHeaderCell>Макс. г/п (т)</TableHeaderCell>
            </TableRow>
          </TableHeader>

          <TableBody>
            {cranes.map((crane) => (
              <TableRow key={crane.name} className='table-row-hover'>
                <TableCell>
                  <Popup
                    content='Перейти к расчету крана'
                    trigger={
                      <Link
                        className='crane-name-link'
                        to={`/cranes/${encodeURIComponent(crane.name)}`}
                      >
                        {crane.manufacturer} {crane.model}
                      </Link>
                    }
                  />
                </TableCell>
                <TableCell>{crane.chassis_type}</TableCell>
                <TableCell className='hide-on-tablet'>
                  {crane.resource_code}
                </TableCell>
                <TableCell className='hide-on-tablet'>
                  {crane.price_per_hour.toLocaleString()}
                </TableCell>
                <TableCell>{crane.max_lifting_capacity}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      ) : (
        <Message info>
          <Message.Header>Не найдено</Message.Header>
          <p>
            Нет кранов, соответствующих вашим текущим фильтрам. Попробуйте
            изменить критерии поиска.
          </p>
        </Message>
      )}
    </>
  )
}

export default CranesList
