import React, { useEffect, useState } from 'react'
import { useParams } from 'react-router-dom'

import { fetchCraneByName } from '@/src/api/cranes'
import CraneCalcView from '@/src/components/CraneCalcView'
import CraneDataView from '@/src/components/CraneDataView'
import './CraneDetail.css'

const CraneDetail = () => {
  const { name } = useParams()
  const [crane, setCrane] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

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
      <CraneDataView crane={crane} />
      <CraneCalcView crane={crane} />
    </main>
  )
}

export default CraneDetail
