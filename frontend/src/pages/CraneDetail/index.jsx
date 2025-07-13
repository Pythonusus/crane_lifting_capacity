import React, { useEffect, useState } from 'react'
import { useParams } from 'react-router-dom'
import { Header } from 'semantic-ui-react'

import { fetchCraneById } from '@/src/api/cranes'
import CraneCalcView from '@/src/components/CraneCalcView'
import CraneDataView from '@/src/components/CraneDataView'
import './CraneDetail.css'

const CraneDetail = () => {
  const { id } = useParams()
  const [crane, setCrane] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    const loadCrane = async () => {
      if (!id) return

      setLoading(true)
      setError(null)

      try {
        const craneData = await fetchCraneById(id)
        setCrane(craneData)
      } catch (error_) {
        setError('Не удалось загрузить кран')
        console.error('Error loading crane:', error_)
      } finally {
        setLoading(false)
      }
    }

    loadCrane()
  }, [id])

  if (loading) {
    return <div>Загрузка...</div>
  }

  if (error) {
    return <div>Ошибка: {error}</div>
  }

  if (!crane) {
    return <div>Кран не найден</div>
  }

  return (
    <main className='crane-detail-main-content'>
      <div className='crane-detail-header'>
        <Header as='h1'>{crane.name}</Header>
      </div>
      <CraneDataView crane={crane} />
      <CraneCalcView crane={crane} />
    </main>
  )
}

export default CraneDetail
