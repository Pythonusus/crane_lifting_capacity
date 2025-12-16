import {
  Document,
  Packer,
  Paragraph,
  TextRun,
  Table,
  TableRow,
  TableCell,
  WidthType,
  AlignmentType,
} from 'docx'
import { saveAs } from 'file-saver'

/**
 * Generate and download a Word document with comparison table results
 * @param {Object} comparisonResults - The comparison results object with results array
 * @param {Object} formData - Form data used for the comparison
 */
export const generateAndDownloadComparisonReport = async (
  comparisonResults,
  formData,
) => {
  if (!comparisonResults || !comparisonResults.results) {
    console.error('No comparison results to export')
    return
  }

  const results = comparisonResults.results || []
  const validResults = results.filter((r) => r.success)

  if (validResults.length === 0) {
    console.error('No valid results to export')
    return
  }

  // Create document
  const doc = new Document({
    sections: [
      {
        properties: {},
        children: [
          // Title
          new Paragraph({
            children: [
              new TextRun({
                text: 'ОТЧЕТ О СРАВНЕНИИ КРАНОВ',
                bold: true,
                size: 32,
              }),
            ],
            alignment: AlignmentType.CENTER,
            spacing: { after: 400 },
          }),

          // Parameters section
          new Paragraph({
            children: [
              new TextRun({
                text: 'ПАРАМЕТРЫ РАСЧЕТА',
                bold: true,
                size: 24,
              }),
            ],
            spacing: { before: 200, after: 200 },
          }),

          // Parameters table
          new Table({
            width: {
              size: 100,
              type: WidthType.PERCENTAGE,
            },
            rows: [
              new TableRow({
                children: [
                  new TableCell({
                    children: [
                      new Paragraph({
                        children: [
                          new TextRun({
                            text: 'Вылет стрелы',
                            bold: true,
                            size: 22,
                          }),
                        ],
                        spacing: { before: 60, after: 60 },
                        indent: { left: 57 },
                      }),
                    ],
                    width: { size: 40, type: WidthType.PERCENTAGE },
                  }),
                  new TableCell({
                    children: [
                      new Paragraph({
                        children: [
                          new TextRun({
                            text: `${formData.boomRadius || 'Н/Д'} м`,
                            size: 22,
                          }),
                        ],
                        spacing: { before: 60, after: 60 },
                        indent: { left: 57 },
                      }),
                    ],
                    width: { size: 60, type: WidthType.PERCENTAGE },
                  }),
                ],
              }),
              ...(formData.equipmentWeight
                ? [
                    new TableRow({
                      children: [
                        new TableCell({
                          children: [
                            new Paragraph({
                              children: [
                                new TextRun({
                                  text: 'Вес строп. оборудования',
                                  bold: true,
                                  size: 22,
                                }),
                              ],
                              spacing: { before: 60, after: 60 },
                              indent: { left: 57 },
                            }),
                          ],
                        }),
                        new TableCell({
                          children: [
                            new Paragraph({
                              children: [
                                new TextRun({
                                  text: `${formData.equipmentWeight} т`,
                                  size: 22,
                                }),
                              ],
                              spacing: { before: 60, after: 60 },
                              indent: { left: 57 },
                            }),
                          ],
                        }),
                      ],
                    }),
                  ]
                : []),
              new TableRow({
                children: [
                  new TableCell({
                    children: [
                      new Paragraph({
                        children: [
                          new TextRun({
                            text: 'Вес груза',
                            bold: true,
                            size: 22,
                          }),
                        ],
                        spacing: { before: 60, after: 60 },
                        indent: { left: 57 },
                      }),
                    ],
                  }),
                  new TableCell({
                    children: [
                      new Paragraph({
                        children: [
                          new TextRun({
                            text: `${formData.payload || 'Н/Д'} т`,
                            size: 22,
                          }),
                        ],
                        spacing: { before: 60, after: 60 },
                        indent: { left: 57 },
                      }),
                    ],
                  }),
                ],
              }),
            ],
          }),

          // Results section
          new Paragraph({
            children: [
              new TextRun({
                text: 'РЕЗУЛЬТАТЫ СРАВНЕНИЯ',
                bold: true,
                size: 24,
              }),
            ],
            spacing: { before: 400, after: 200 },
          }),

          // Comparison table
          new Table({
            width: {
              size: 100,
              type: WidthType.PERCENTAGE,
            },
            rows: [
              // Header row
              new TableRow({
                children: [
                  new TableCell({
                    children: [
                      new Paragraph({
                        children: [
                          new TextRun({
                            text: 'Кран',
                            bold: true,
                            size: 22,
                          }),
                        ],
                        alignment: AlignmentType.CENTER,
                        spacing: { before: 60, after: 60 },
                      }),
                    ],
                    width: { size: 20, type: WidthType.PERCENTAGE },
                  }),
                  new TableCell({
                    children: [
                      new Paragraph({
                        children: [
                          new TextRun({
                            text: 'Тип стрелы',
                            bold: true,
                            size: 22,
                          }),
                        ],
                        alignment: AlignmentType.CENTER,
                        spacing: { before: 60, after: 60 },
                      }),
                    ],
                    width: { size: 15, type: WidthType.PERCENTAGE },
                  }),
                  new TableCell({
                    children: [
                      new Paragraph({
                        children: [
                          new TextRun({
                            text: 'Стоимость маш.-ч (₽)',
                            bold: true,
                            size: 22,
                          }),
                        ],
                        alignment: AlignmentType.CENTER,
                        spacing: { before: 60, after: 60 },
                      }),
                    ],
                    width: { size: 15, type: WidthType.PERCENTAGE },
                  }),
                  new TableCell({
                    children: [
                      new Paragraph({
                        children: [
                          new TextRun({
                            text: 'Г/П на вылете (т)',
                            bold: true,
                            size: 22,
                          }),
                        ],
                        alignment: AlignmentType.CENTER,
                        spacing: { before: 60, after: 60 },
                      }),
                    ],
                    width: { size: 15, type: WidthType.PERCENTAGE },
                  }),
                  new TableCell({
                    children: [
                      new Paragraph({
                        children: [
                          new TextRun({
                            text: 'Коэф. запаса',
                            bold: true,
                            size: 22,
                          }),
                        ],
                        alignment: AlignmentType.CENTER,
                        spacing: { before: 60, after: 60 },
                      }),
                    ],
                    width: { size: 15, type: WidthType.PERCENTAGE },
                  }),
                  new TableCell({
                    children: [
                      new Paragraph({
                        children: [
                          new TextRun({
                            text: 'Запас Г/П (т)',
                            bold: true,
                            size: 22,
                          }),
                        ],
                        alignment: AlignmentType.CENTER,
                        spacing: { before: 60, after: 60 },
                      }),
                    ],
                    width: { size: 20, type: WidthType.PERCENTAGE },
                  }),
                ],
              }),
              // Data rows
              ...validResults.map((result) => {
                const crane = result.crane
                const calcResult = result.result
                const craneName = `${crane.manufacturer} ${crane.model}`
                const boomLength = result.boomLength || 'Н/Д'
                const price = crane.base_price
                  ? `${crane.base_price.toFixed(2)}`
                  : 'Н/Д'
                const liftingCapacity = calcResult.lifting_capacity
                  ? calcResult.lifting_capacity.toFixed(2)
                  : 'Н/Д'
                const safetyFactor = calcResult.safety_factor
                  ? calcResult.safety_factor.toFixed(2)
                  : 'Н/Д'
                const remainingLc = calcResult.remaining_lc
                  ? calcResult.remaining_lc.toFixed(2)
                  : 'Н/Д'

                return new TableRow({
                  children: [
                    new TableCell({
                      children: [
                        new Paragraph({
                          children: [
                            new TextRun({
                              text: craneName,
                              size: 20,
                            }),
                          ],
                          spacing: { before: 60, after: 60 },
                          indent: { left: 57 },
                        }),
                      ],
                    }),
                    new TableCell({
                      children: [
                        new Paragraph({
                          children: [
                            new TextRun({
                              text: boomLength,
                              size: 20,
                            }),
                          ],
                          alignment: AlignmentType.CENTER,
                          spacing: { before: 60, after: 60 },
                        }),
                      ],
                    }),
                    new TableCell({
                      children: [
                        new Paragraph({
                          children: [
                            new TextRun({
                              text: price,
                              size: 20,
                            }),
                          ],
                          alignment: AlignmentType.CENTER,
                          spacing: { before: 60, after: 60 },
                        }),
                      ],
                    }),
                    new TableCell({
                      children: [
                        new Paragraph({
                          children: [
                            new TextRun({
                              text: liftingCapacity,
                              size: 20,
                            }),
                          ],
                          alignment: AlignmentType.CENTER,
                          spacing: { before: 60, after: 60 },
                        }),
                      ],
                    }),
                    new TableCell({
                      children: [
                        new Paragraph({
                          children: [
                            new TextRun({
                              text: safetyFactor,
                              size: 20,
                            }),
                          ],
                          alignment: AlignmentType.CENTER,
                          spacing: { before: 60, after: 60 },
                        }),
                      ],
                    }),
                    new TableCell({
                      children: [
                        new Paragraph({
                          children: [
                            new TextRun({
                              text: remainingLc,
                              size: 20,
                            }),
                          ],
                          alignment: AlignmentType.CENTER,
                          spacing: { before: 60, after: 60 },
                        }),
                      ],
                    }),
                  ],
                })
              }),
            ],
          }),

          // Best cranes section
          ...(comparisonResults.cheapestCrane ||
          comparisonResults.smallestSafetyFactorCrane
            ? [
                new Paragraph({
                  children: [
                    new TextRun({
                      text: 'ЛУЧШИЕ ВАРИАНТЫ',
                      bold: true,
                      size: 24,
                    }),
                  ],
                  spacing: { before: 400, after: 200 },
                }),
                ...(comparisonResults.cheapestCrane
                  ? [
                      new Paragraph({
                        children: [
                          new TextRun({
                            text: (() => {
                              const cheapest = comparisonResults.cheapestCrane
                              const boomLengthText = cheapest.boomLength
                                ? ` (${cheapest.boomLength})`
                                : ''
                              const priceText =
                                cheapest.price?.toFixed(2) || 'Н/Д'
                              return `Наименьшая стоимость маш.-ч: ${cheapest.name}${boomLengthText} - ${priceText} ₽`
                            })(),
                            size: 22,
                          }),
                        ],
                        spacing: { before: 60, after: 60 },
                      }),
                    ]
                  : []),
                ...(comparisonResults.smallestSafetyFactorCrane
                  ? [
                      new Paragraph({
                        children: [
                          new TextRun({
                            text: (() => {
                              const smallest =
                                comparisonResults.smallestSafetyFactorCrane
                              const boomLengthText = smallest.boomLength
                                ? ` (${smallest.boomLength})`
                                : ''
                              const safetyFactorText =
                                smallest.safetyFactor?.toFixed(2) || 'Н/Д'
                              return `Наименьший коэффициент запаса: ${smallest.name}${boomLengthText} - ${safetyFactorText}`
                            })(),
                            size: 22,
                          }),
                        ],
                        spacing: { before: 60, after: 60 },
                      }),
                    ]
                  : []),
              ]
            : []),

          // Footer
          new Paragraph({
            children: [
              new TextRun({
                text: `Отчет создан: ${new Date().toLocaleString('ru-RU')}`,
                size: 20,
                italics: true,
              }),
            ],
            alignment: AlignmentType.RIGHT,
            spacing: { before: 400 },
          }),
        ],
      },
    ],
  })

  // Generate and download
  try {
    const blob = await Packer.toBlob(doc)

    const filename = `Сравнение_кранов_${new Date().toISOString().split('T')[0]}.docx`
    saveAs(blob, filename)
  } catch (error) {
    console.error('Error generating comparison report:', error)
    throw error
  }
}
