import { useState } from 'react'
import {
  Container,
  Header,
  Form,
  Button,
  Segment,
  Message,
  Dimmer,
  Loader,
} from 'semantic-ui-react'
import 'semantic-ui-css/semantic.min.css'
import './App.css'

function App() {
  const [numberA, setNumberA] = useState(0)
  const [numberB, setNumberB] = useState(0)
  const [result, setResult] = useState(null)
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState(null)

  const handleCalculate = async () => {
    setIsLoading(true)
    setError(null)

    try {
      const response = await fetch('/process', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          first_number: Number.parseFloat(numberA),
          second_number: Number.parseFloat(numberB),
        }),
      })

      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`)
      }

      const data = await response.json()
      setResult(data.result)
    } catch (error_) {
      setError(`Error: ${error_.message}`)
      console.error('Calculation error:', error_)
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <Container text className='calculator-container'>
      <Header as='h1' textAlign='center'>
        Simple Calculator
      </Header>

      <Segment raised>
        <Dimmer active={isLoading} inverted>
          <Loader>Calculating...</Loader>
        </Dimmer>

        <Form>
          <Form.Field>
            <label htmlFor='firstNumber'>First Number</label>
            <Form.Input
              id='firstNumber'
              type='number'
              value={numberA}
              onChange={(e) => setNumberA(e.target.value)}
              fluid
            />
          </Form.Field>

          <Form.Field>
            <label htmlFor='secondNumber'>Second Number</label>
            <Form.Input
              id='secondNumber'
              type='number'
              value={numberB}
              onChange={(e) => setNumberB(e.target.value)}
              fluid
            />
          </Form.Field>

          <Button primary fluid onClick={handleCalculate} disabled={isLoading}>
            Calculate
          </Button>
        </Form>
      </Segment>

      {result !== null && (
        <Message positive>
          <Message.Header>Result</Message.Header>
          <p>{result}</p>
        </Message>
      )}

      {error && (
        <Message negative>
          <Message.Header>Error</Message.Header>
          <p>{error}</p>
        </Message>
      )}
    </Container>
  )
}

export default App
