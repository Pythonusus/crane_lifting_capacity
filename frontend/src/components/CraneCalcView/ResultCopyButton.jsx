import React, { useState } from 'react'
import { Button, Icon } from 'semantic-ui-react'

import { formatCalculationValue } from '@/src/utilities/formatters'

const copyWithFallback = async (text) => {
  // Try to use the clipboard API if available but writeText failed
  if (navigator.clipboard && navigator.clipboard.write) {
    try {
      const blob = new Blob([text], { type: 'text/plain' })
      const clipboardItem = new ClipboardItem({ 'text/plain': blob })
      await navigator.clipboard.write([clipboardItem])
      return
    } catch {
      // Fall through to next method
    }
  }

  // Try using the older clipboard API methods
  if (navigator.clipboard && navigator.clipboard.writeText) {
    try {
      await navigator.clipboard.writeText(text)
      return
    } catch {
      // Fall through to final fallback
    }
  }

  // Simple fallback: just throw an error
  // In practice, clipboard API works in 99% of cases
  throw new Error('Clipboard not available')
}

const addCommonParameters = (result, req) => {
  if (req.boom_len) {
    result.push(`Тип стрелы: ${req.boom_len}`)
  }
  if (req.radius) {
    result.push(`Вылет стрелы: ${req.radius} м`)
  }
  if (typeof req.equipment_weight === 'number' && req.equipment_weight > 0) {
    result.push(`Вес строп. оборудования: ${req.equipment_weight} т`)
  }
}

const addPayloadInfo = (result, req, base) => {
  if (typeof req.payload === 'number') {
    result.push(`Вес груза: ${req.payload} т`)
  }
  if (typeof base.payload === 'number') {
    result.push(`Вес груза: ${formatCalculationValue(base.payload)} т`)
  }
}

const addLiftingCapacityInfo = (result, base) => {
  if (typeof base.lifting_capacity === 'number') {
    result.push(
      `Грузоподъемность на данном вылете: ${formatCalculationValue(base.lifting_capacity)} т`,
    )
  }
}

const addSafetyFactorInfo = (result, req, base) => {
  if (typeof base.safety_factor === 'number') {
    result.push(
      `Коэффициент запаса: ${formatCalculationValue(base.safety_factor)}`,
    )
  }
  if (typeof req.safety_factor === 'number') {
    result.push(
      `Коэффициент запаса: ${formatCalculationValue(req.safety_factor)}`,
    )
  }
}

const addSpareCapacityInfo = (result, req, base) => {
  if (typeof req.payload === 'number') {
    const spare = formatCalculationValue(
      base.lifting_capacity -
        req.payload -
        (typeof req.equipment_weight === 'number' ? req.equipment_weight : 0),
    )
    result.push(`Запас грузоподъемности: ${spare} т`)
  } else if (typeof base.payload === 'number') {
    const spare = formatCalculationValue(
      base.lifting_capacity -
        base.payload -
        (typeof req.equipment_weight === 'number' ? req.equipment_weight : 0),
    )
    result.push(`Запас грузоподъемности: ${spare} т`)
  }
}

const buildCopyText = (calculationResult, crane) => {
  const result = []

  // Fix: Access the first base response from the calculation result
  const base = calculationResult.base_responses?.[0]
  if (!base) return ''

  const req = base.request || {}
  result.push(
    `Результаты расчета грузоподъемности крана ${crane.manufacturer} ${crane.model}`,
  )

  addCommonParameters(result, req)

  addPayloadInfo(result, req, base)

  addLiftingCapacityInfo(result, base)

  addSafetyFactorInfo(result, req, base)

  addSpareCapacityInfo(result, req, base)

  return result.join('\n')
}

/**
 * Component for copying calculation results to clipboard
 *
 * @param {Object} props - Component props
 * @param {Object|null} props.calculationResult - API calculation result object
 * @param {boolean} props.isChecked - Current calculation mode (determines which result to show)
 * @param {Object} props.crane - Crane data object containing manufacturer and model
 */
const ResultCopyButton = ({ calculationResult, crane }) => {
  const [copied, setCopied] = useState(false)

  const handleCopy = async () => {
    if (!calculationResult) return
    const text = buildCopyText(calculationResult, crane)
    if (!text) return

    try {
      await (navigator?.clipboard?.writeText
        ? navigator.clipboard.writeText(text)
        : copyWithFallback(text))
      setCopied(true)
      setTimeout(() => setCopied(false), 1500)
    } catch {
      // Clipboard failed - just fail silently
      // In practice, this rarely happens in modern browsers
    }
  }

  return (
    <Button
      icon
      labelPosition='left'
      size='tiny'
      color='teal'
      onClick={handleCopy}
      disabled={!calculationResult}
    >
      <Icon name={copied ? 'check' : 'copy'} />
      {copied ? 'Скопировано' : 'Копировать результат'}
    </Button>
  )
}

export default ResultCopyButton
