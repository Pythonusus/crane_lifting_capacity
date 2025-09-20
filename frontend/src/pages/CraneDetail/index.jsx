import React, { useEffect, useState } from 'react'
import { useParams, useLocation } from 'react-router-dom'
import { Container, Header, Icon, Message } from 'semantic-ui-react'

import { fetchCraneByName } from '@/src/api/cranes'
import CalculationForm from '@/src/components/CalculationForm'
import CalculationResults from '@/src/components/CalculationResults'
import CraneDataView from '@/src/components/CraneDataView'
import useCalculationForm from '@/src/hooks/useCalculationForm'
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

  // Use calculation form hook
  const {
    calculationMode,
    setCalculationMode,
    formData,
    errors,
    validationErrors,
    isSubmitting,
    calculationResult,
    handleInputChange,
    handleSubmit,
    handleClearForm,
  } = useCalculationForm(crane, initialFormData, initialMode, initialResult)

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
      <div className='calc-view-container'>
        <hr className='calc-view-divider' />
        <Header
          as='h2'
          textAlign='center'
          className='calc-view-header font-size-3'
        >
          Расcчитать грузоподъемность крана
        </Header>
        <hr className='calc-view-divider' />
        <div className='calc-input-and-result-container'>
          <CalculationForm
            crane={crane}
            formData={formData}
            errors={errors}
            validationErrors={validationErrors}
            isSubmitting={isSubmitting}
            calculationMode={calculationMode}
            onInputChange={handleInputChange}
            onSubmit={handleSubmit}
            onClear={handleClearForm}
            onModeChange={setCalculationMode}
          />
          <CalculationResults
            calculationResult={calculationResult}
            calculationMode={calculationMode}
            crane={crane}
          />
        </div>
      </div>
    </main>
  )
}

export default CraneDetail
