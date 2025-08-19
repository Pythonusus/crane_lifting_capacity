import React, { useEffect, useState } from 'react'
import {
  Button,
  Dropdown,
  Header,
  Icon,
  Input,
  Popup,
  Segment,
} from 'semantic-ui-react'

import {
  fetchChassisTypes,
  fetchManufacturers,
  fetchSortOptions,
} from '@/src/api/cranes'

import './CranesFilterSidebar.css'

// Function to validate numeric input and return error message if invalid
const validateNumericInput = (inputValue) => {
  if (!inputValue) return '' // Empty value is allowed

  // Check if input contains only valid characters
  if (!/^[0-9.,-]*$/.test(inputValue)) {
    return 'Разрешены только цифры, точка, запятая и знак минус'
  }

  // Check for multiple decimal separators
  const commaCount = (inputValue.match(/,/g) || []).length
  const dotCount = (inputValue.match(/\./g) || []).length
  if (commaCount + dotCount > 1) {
    return 'Используйте только один десятичный разделитель'
  }

  // Check for minus sign in wrong position
  if (inputValue.includes('-') && !inputValue.startsWith('-')) {
    return 'Знак минус может быть только в начале числа'
  }

  // Check for multiple minus signs
  if ((inputValue.match(/-/g) || []).length > 1) {
    return 'Используйте только один знак минус'
  }

  return '' // No errors
}

const CranesFilterSidebar = ({ filters, onFiltersChange, onClearFilters }) => {
  const [chassisTypes, setChassisTypes] = useState([])
  const [manufacturers, setManufacturers] = useState([])
  const [sortOptions, setSortOptions] = useState([])
  const [validationErrors, setValidationErrors] = useState({})

  // Fetch chassis types on component mount
  useEffect(() => {
    const loadChassisTypes = async () => {
      try {
        const chassis = await fetchChassisTypes()
        setChassisTypes(chassis)
      } catch (error_) {
        console.error('Failed to load chassis types:', error_)
      }
    }
    loadChassisTypes()
  }, [])

  // Fetch manufacturers on component mount
  useEffect(() => {
    const loadManufacturers = async () => {
      try {
        const manufacturers = await fetchManufacturers()
        setManufacturers(manufacturers)
      } catch (error_) {
        console.error('Failed to load manufacturers:', error_)
      }
    }
    loadManufacturers()
  }, [])

  // Fetch sort options on component mount
  useEffect(() => {
    const loadSortOptions = async () => {
      try {
        const options = await fetchSortOptions()
        setSortOptions(options)
      } catch (error_) {
        console.error('Failed to load sort options:', error_)
      }
    }
    loadSortOptions()
  }, [])

  const handleSearchChange = (e, { value }) => {
    onFiltersChange((prev) => ({ ...prev, model: value }))
  }

  const handleChassisTypeChange = (e, { value }) => {
    onFiltersChange((prev) => ({ ...prev, chassis_type: value }))
  }

  const handleManufacturerChange = (e, { value }) => {
    onFiltersChange((prev) => ({ ...prev, manufacturer: value }))
  }

  const handleMinMaxLiftingCapacityChange = (e, { value }) => {
    // Filter out invalid characters - only allow numbers, dots, and commas
    const filteredValue = value.replaceAll(/[^0-9.,]/g, '')

    // Only update if the value is valid or empty
    if (filteredValue === value || filteredValue === '') {
      const error = validateNumericInput(filteredValue)
      setValidationErrors((prev) => ({ ...prev, min_max_lc: error }))
      // Normalize input: convert comma to dot for internal processing
      const normalizedValue = filteredValue.replaceAll(',', '.')
      onFiltersChange((prev) => ({ ...prev, min_max_lc: normalizedValue }))
    }
  }

  const handleMaxMaxLiftingCapacityChange = (e, { value }) => {
    // Filter out invalid characters - only allow numbers, dots, and commas
    const filteredValue = value.replaceAll(/[^0-9.,]/g, '')

    // Only update if the value is valid or empty
    if (filteredValue === value || filteredValue === '') {
      const error = validateNumericInput(filteredValue)
      setValidationErrors((prev) => ({ ...prev, max_max_lc: error }))
      // Normalize input: convert comma to dot for internal processing
      const normalizedValue = filteredValue.replaceAll(',', '.')
      onFiltersChange((prev) => ({ ...prev, max_max_lc: normalizedValue }))
    }
  }

  const handleSortByChange = (e, { value }) => {
    onFiltersChange((prev) => ({ ...prev, sortBy: value }))
  }

  const getChassisTypeOptions = () => {
    return [
      { key: '', text: 'Все типы шасси', value: '' },
      ...chassisTypes.map((type) => ({
        key: type,
        text: type.charAt(0).toUpperCase() + type.slice(1),
        value: type,
      })),
    ]
  }

  const getManufacturerOptions = () => {
    return [
      { key: '', text: 'Все производители', value: '' },
      ...manufacturers.map((manufacturer) => ({
        key: manufacturer,
        text: manufacturer,
        value: manufacturer,
      })),
    ]
  }

  return (
    <Segment className='cranes-filter-sidebar'>
      <div className='filter-sidebar-content'>
        <Header as='h3' className='filter-sidebar-header font-size-3'>
          <Header.Content>Фильтры и сортировка</Header.Content>
        </Header>

        {/* Search Input */}
        <div className='filter-section'>
          <Header as='h4' size='small' className='mb-5'>
            Поиск по названию модели
          </Header>
          <Popup
            content='Пример: РДК250'
            trigger={
              <Input
                fluid
                icon='search'
                iconPosition='left'
                placeholder='Искать'
                value={filters.model || ''}
                onChange={handleSearchChange}
              />
            }
            position='top left'
            size='small'
          />
        </div>

        {/* Chassis Type Filter */}
        <div className='filter-section'>
          <Header as='h4' size='small' className='mb-5'>
            Тип шасси
          </Header>
          <Dropdown
            fluid
            selection
            placeholder='Выберите тип шасси'
            options={getChassisTypeOptions()}
            value={filters.chassis_type || ''}
            onChange={handleChassisTypeChange}
          />
        </div>

        {/* Manufacturer Filter */}
        <div className='filter-section'>
          <Header as='h4' size='small' className='mb-5'>
            Производитель
          </Header>
          <Dropdown
            fluid
            selection
            placeholder='Выберите производителя'
            options={getManufacturerOptions()}
            value={filters.manufacturer || ''}
            onChange={handleManufacturerChange}
          />
        </div>

        {/* Min max lifting capacity Filter */}
        <div className='filter-section'>
          <Header as='h4' size='small' className='mb-5'>
            Макс грузоподъемность (т)
          </Header>
          <div className='filter-section-inputs'>
            <Popup
              content={validationErrors.min_max_lc}
              open={!!validationErrors.min_max_lc}
              position='left center'
              color='red'
              size='small'
              onClose={() =>
                setValidationErrors((prev) => ({ ...prev, min_max_lc: '' }))
              }
              trigger={
                <Input
                  fluid
                  placeholder='Не менее'
                  value={filters.min_max_lc || ''}
                  onChange={handleMinMaxLiftingCapacityChange}
                  error={!!validationErrors.min_max_lc}
                />
              }
            />
            <Popup
              content={validationErrors.max_max_lc}
              open={!!validationErrors.max_max_lc}
              position='left center'
              color='red'
              size='small'
              onClose={() =>
                setValidationErrors((prev) => ({ ...prev, max_max_lc: '' }))
              }
              trigger={
                <Input
                  className='m-top'
                  fluid
                  placeholder='Не более'
                  value={filters.max_max_lc || ''}
                  onChange={handleMaxMaxLiftingCapacityChange}
                  error={!!validationErrors.max_max_lc}
                />
              }
            />
          </div>
        </div>

        {/* Sort By Filter */}
        <div className='filter-section'>
          <Header as='h4' size='small' className='mb-5'>
            Сортировка
          </Header>
          <Dropdown
            fluid
            selection
            placeholder='Выберите сортировку'
            options={sortOptions}
            value={filters.sortBy}
            onChange={handleSortByChange}
          />
        </div>

        {/* Clear Filters Button */}
        <div className='clear-filters-section'>
          <Button
            fluid
            icon
            labelPosition='center'
            size='small'
            onClick={() => {
              setValidationErrors({})
              onClearFilters()
            }}
            disabled={
              (!filters.model || filters.model === '') &&
              (!filters.chassis_type || filters.chassis_type === '') &&
              (!filters.manufacturer || filters.manufacturer === '') &&
              (!filters.min_max_lc || filters.min_max_lc === '') &&
              (!filters.max_max_lc || filters.max_max_lc === '') &&
              filters.sortBy === 'displayNameAsc'
            }
            color='blue'
          >
            <Icon name='refresh' />
            Сбросить фильтры
          </Button>
        </div>
      </div>
    </Segment>
  )
}

export default CranesFilterSidebar
