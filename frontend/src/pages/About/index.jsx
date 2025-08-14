import React from 'react'
import {
  Container,
  Header,
  Segment,
  List,
  Icon,
  Grid,
  Card,
} from 'semantic-ui-react'
import './About.css'

const About = () => (
  <Container className='about-container'>
    <Segment raised>
      <Header as='h1' className='font-size-1'>
        Калькулятор грузоподъемности кранов
      </Header>

      <p className='about-intro-text'>
        Добро пожаловать в приложение для расчета грузоподъемности строительных
        кранов. Данная система предназначена для инженеров, проектировщиков и
        специалистов строительной отрасли, которым необходимо быстро и точно
        определить параметры работы строительного оборудования.
      </p>
    </Segment>

    <Grid stackable>
      <Grid.Row>
        <Grid.Column width={8}>
          <Card fluid>
            <Card.Content>
              <Card.Header>
                <Icon name='search' color='blue' />
                Поиск и фильтрация кранов
              </Card.Header>
              <Card.Description>
                <List bulleted className='left-text'>
                  <List.Item>
                    Интерактивная таблица со всеми доступными кранами
                  </List.Item>
                  <List.Item>
                    Фильтрация по производителю, модели и типу шасси
                  </List.Item>
                  <List.Item>
                    Поиск по диапазону максимальной грузоподъемности
                  </List.Item>
                  <List.Item>Сортировка по различным параметрам</List.Item>
                </List>
              </Card.Description>
            </Card.Content>
          </Card>
        </Grid.Column>

        <Grid.Column width={8}>
          <Card fluid>
            <Card.Content>
              <Card.Header>
                <Icon name='calculator' color='violet' />
                Расчетный модуль
              </Card.Header>
              <Card.Description>
                <List bulleted className='left-text'>
                  <List.Item>
                    Два режима расчета: по заданному грузу и по коэффициенту
                    запаса
                  </List.Item>
                  <List.Item>
                    Удобный ввод исходных данных с защитой от ошибок
                  </List.Item>
                  <List.Item>
                    Автоматический расчет грузоподъемности на заданном вылете
                  </List.Item>
                  <List.Item>
                    Определение коэффициента запаса и запаса грузоподъемности
                  </List.Item>
                </List>
              </Card.Description>
            </Card.Content>
          </Card>
        </Grid.Column>
      </Grid.Row>

      <Grid.Row>
        <Grid.Column width={8}>
          <Card fluid>
            <Card.Content>
              <Card.Header>
                <Icon name='download' color='orange ' />
                Экспорт результатов
              </Card.Header>
              <Card.Description>
                <List bulleted className='left-text'>
                  <List.Item>
                    Быстрое копирование результатов расчета в буфер обмена
                  </List.Item>
                  <List.Item>
                    Автоматическое формирование отчета в формате DOC
                  </List.Item>
                </List>
              </Card.Description>
            </Card.Content>
          </Card>
        </Grid.Column>

        <Grid.Column width={8}>
          <Card fluid>
            <Card.Content>
              <Card.Header>
                <Icon name='history' color='teal' />
                История расчетов
              </Card.Header>
              <Card.Description>
                <List bulleted className='left-text'>
                  <List.Item>
                    Сохранение всех выполненных расчетов в локальном хранилище
                  </List.Item>
                  <List.Item>Быстрый доступ к предыдущим результатам</List.Item>
                </List>
              </Card.Description>
            </Card.Content>
          </Card>
        </Grid.Column>
      </Grid.Row>

      <Grid.Row>
        <Grid.Column>
          <Card fluid>
            <Card.Content>
              <Card.Header className='font-size-4 left-text'>
                Примечания:
              </Card.Header>
              <Card.Description>
                <List bulleted className='left-text'>
                  <List.Item>
                    Таблицы грузоподъемности, используемые в приложении, взяты
                    из технических данных кранов с официальных сайтов
                    производителей и дистрибьюторов.
                  </List.Item>
                  <List.Item>
                    В соответствии с рекомендациями технических данных,
                    окончательную грузоподъемность крана следует определять по
                    паспорту крана.
                  </List.Item>
                  <List.Item>
                    Окончательный выбор строительной техники для конкретных
                    условий всегда остается за инженером.
                  </List.Item>
                </List>
              </Card.Description>
            </Card.Content>
          </Card>
        </Grid.Column>
      </Grid.Row>
    </Grid>
  </Container>
)

export default About
