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

import { fetchChassisTypes, fetchManufacturers } from '@/src/api/cranes'

import './CranesFilterSidebar.css'

const getSortByOptions = () => {
  return [
    {
      key: 'maxCapacityAsc',
      text: 'Макс г/п ↑',
      value: 'maxCapacityAsc',
    },
    {
      key: 'maxCapacityDesc',
      text: 'Макс г/п ↓',
      value: 'maxCapacityDesc',
    },
    {
      key: 'displayNameAsc',
      text: 'Название крана (А-Я)',
      value: 'displayNameAsc',
    },
    {
      key: 'displayNameDesc',
      text: 'Название крана (Я-А)',
      value: 'displayNameDesc',
    },
    {
      key: 'pricePerHourAsc',
      text: 'Стоимость маш.-ч ↑',
      value: 'pricePerHourAsc',
    },
    {
      key: 'pricePerHourDesc',
      text: 'Стоимость маш.-ч ↓',
      value: 'pricePerHourDesc',
    },
  ]
}

const CranesFilterSidebar = ({ filters, onFiltersChange, onClearFilters }) => {
  const [chassisTypes, setChassisTypes] = useState([])
  const [manufacturers, setManufacturers] = useState([])

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

  const handleSearchChange = (e, { value }) => {
    onFiltersChange((prev) => ({ ...prev, name: value }))
  }

  const handleChassisTypeChange = (e, { value }) => {
    onFiltersChange((prev) => ({ ...prev, chassis_type: value }))
  }

  const handleManufacturerChange = (e, { value }) => {
    onFiltersChange((prev) => ({ ...prev, manufacturer: value }))
  }

  const handleMinMaxLiftingCapacityChange = (e, { value }) => {
    onFiltersChange((prev) => ({ ...prev, min_max_lc: value }))
  }

  const handleMaxMaxLiftingCapacityChange = (e, { value }) => {
    onFiltersChange((prev) => ({ ...prev, max_max_lc: value }))
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
        <Header as='h3' className='filter-sidebar-header'>
          <Header.Content>Фильтры и сортировка</Header.Content>
        </Header>

        {/* Search Input */}
        <div className='filter-section'>
          <Header as='h4' size='small'>
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
                value={filters.name || ''}
                onChange={handleSearchChange}
              />
            }
            position='top left'
            size='small'
          />
        </div>

        {/* Chassis Type Filter */}
        <div className='filter-section'>
          <Header as='h4' size='small'>
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
          <Header as='h4' size='small'>
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
          <Header as='h4' size='small'>
            Макс грузоподъемность (т)
          </Header>
          <div className='filter-section-inputs'>
            <Input
              fluid
              placeholder='Не менее'
              value={filters.min_max_lc || ''}
              onChange={handleMinMaxLiftingCapacityChange}
            />
            <Input
              className='m-top'
              fluid
              placeholder='Не более'
              value={filters.max_max_lc || ''}
              onChange={handleMaxMaxLiftingCapacityChange}
            />
          </div>
        </div>

        {/* Sort By Filter */}
        <div className='filter-section'>
          <Header as='h4' size='small'>
            Сортировка
          </Header>
          <Dropdown
            fluid
            selection
            placeholder='Выберите сортировку'
            options={getSortByOptions()}
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
            onClick={onClearFilters}
            disabled={
              (!filters.name || filters.name === '') &&
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
