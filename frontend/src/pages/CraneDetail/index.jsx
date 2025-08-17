import React, { useEffect, useState } from 'react'
import { useParams, useLocation } from 'react-router-dom'
import { Container, Header, Icon, Message } from 'semantic-ui-react'

import { fetchCraneByName } from '@/src/api/cranes'
import CraneCalcView from '@/src/components/CraneCalcView'
import CraneDataView from '@/src/components/CraneDataView'
import './CraneDetail.css'

const CraneDetail = () => {
  const { name } = useParams()
  const location = useLocation()
  const [crane, setCrane] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  // Extract initial form data from navigation state
  const initialFormData = location.state?.initialFormData || null
  const initialMode = location.state?.initialMode || 'safety_factor'
  const initialResult = location.state?.initialResult || null

  useEffect(() => {
    const loadCrane = async () => {
      if (!name) return

      setLoading(true)
      setError(null)

      try {
        // Decode the name parameter since React Router automatically decodes it
        const decodedName = decodeURIComponent(name)
        const craneData = await fetchCraneByName(decodedName)
        setCrane(craneData)
      } catch (error_) {
        setError('Не удалось загрузить кран')
        console.error('Error loading crane:', error_)
      } finally {
        setLoading(false)
      }
    }

    loadCrane()
  }, [name])

  if (loading) {
    return (
      <Container className='m-top'>
        <Icon name='spinner' loading size='huge' />
        <Header as='h2' className='loading-header'>
          Загружаем кран...
        </Header>
      </Container>
    )
  }

  if (error) {
    return (
      <Container className='m-top'>
        <Message negative>
          <Message.Header>Ошибка</Message.Header>
          <p>{error}</p>
        </Message>
      </Container>
    )
  }

  return (
    <main className='crane-detail-main-content'>
      <CraneDataView crane={crane} />
      <CraneCalcView
        crane={crane}
        initialFormData={initialFormData}
        initialMode={initialMode}
        initialResult={initialResult}
      />
    </main>
  )
}

export default CraneDetail
