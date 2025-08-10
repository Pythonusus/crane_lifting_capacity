import React, { useState } from 'react'
import { Button, Icon } from 'semantic-ui-react'

const addInputContext = (parts, base, crane) => {
  const req = base.request || {}

  // Add request data
  parts.push(
    `Результаты расчета грузоподъемности крана ${crane.manufacturer} ${crane.model}`,
  )

  if (req.boom_len) {
    parts.push(`Тип стрелы: ${req.boom_len}`)
  }
  if (req.radius) {
    parts.push(`Вылет стрелы: ${req.radius} м`)
  }
  if (typeof req.equipment_weight === 'number' && req.equipment_weight > 0) {
    parts.push(`Вес строп. оборудования: ${req.equipment_weight} т`)
  }
  if (typeof req.payload === 'number') {
    parts.push(`Вес груза: ${req.payload} т`)
  }
  if (typeof req.safety_factor === 'number') {
    parts.push(`Коэффициент запаса: ${req.safety_factor}`)
  }
}

const addLiftingCapacity = (parts, base) => {
  if (typeof base.lifting_capacity === 'number') {
    parts.push(
      `Грузоподъемность на данном вылете: ${base.lifting_capacity.toFixed(2)} т`,
    )
  }
}

const addPayloadResult = (parts, base) => {
  if (typeof base.payload === 'number') {
    parts.push(`Допустимый вес груза: ${base.payload.toFixed(2)} т`)
  }
}

const addSafetyFactorResults = (parts, base) => {
  const req = base.request || {}
  if (typeof req.payload === 'number') {
    const spare = (
      base.lifting_capacity -
      req.payload -
      (typeof req.equipment_weight === 'number' ? req.equipment_weight : 0)
    ).toFixed(2)
    parts.push(`Запас грузоподъемности: ${spare} т`)
  }

  if (typeof base.safety_factor === 'number') {
    parts.push(`Коэффициент запаса: ${base.safety_factor.toFixed(2)}`)
  }
}

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

/**
 * Component for copying calculation results to clipboard
 *
 * @param {Object} props - Component props
 * @param {Object|null} props.calculationResult - API calculation result object
 * @param {boolean} props.isChecked - Current calculation mode (determines which result to show)
 * @param {Object} props.crane - Crane data object containing manufacturer and model
 */
const ResultCopyButton = ({ calculationResult, isChecked, crane }) => {
  const [copied, setCopied] = useState(false)

  const buildCopyText = () => {
    if (!calculationResult) return ''
    const base = calculationResult.base_responses?.[0]
    if (!base) return ''

    return buildResultText(base)
  }

  const buildResultText = (base) => {
    const parts = []

    // Add input context with crane info
    addInputContext(parts, base, crane)

    // Add main result
    addLiftingCapacity(parts, base)

    // Add secondary result based on mode
    addSecondaryResults(parts, base)

    return parts.join('\n')
  }

  const addSecondaryResults = (parts, base) => {
    if (isChecked) {
      addPayloadResult(parts, base)
    } else {
      addSafetyFactorResults(parts, base)
    }
  }

  const handleCopy = async () => {
    if (!calculationResult) return
    const text = buildCopyText()
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
