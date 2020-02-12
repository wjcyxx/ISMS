// 监控预警
// var chart = Highcharts.chart('equipmentStatus', {
//     chart: {
//         backgroundColor: 'transparent',
//         type: 'pie',
//         spacing: [0, 100, 50, 0]
//     },
//     title: {
//         floating: true,
//         text: null,
//         style: {
//             fontSize: '20px',
//             fontWeight: '700',
//             color: "#fff"
//         }
//     },
//     tooltip: {
//         pointFormat: '<b>{point.y}</b>人'
//     },
//     legend: { //图例配置
//         verticalAlign: 'top',
//         y: 20,
//         x: 0,
//         align: 'left',
//         layout: 'vertical',
//         itemStyle: {
//             color: '#A3AAC9',
//             fontWeight: '700',
//             fontSize: '14px'
//         },
//         itemHoverStyle: {
//             color: '#fff'
//         }
//     },
//     plotOptions: {
//         pie: {
//             allowPointSelect: true,
//             cursor: 'pointer',
//             dataLabels: {
//                 enabled: false
//             },
//             showInLegend: true
//         }
//     },
//     series: [{
//         name: 'Brands',
//         innerSize: '80%',
//         colorByPoint: true,
//         data: [{
//             name: '环境',
//             y: 90
//         }, {
//             name: '人员',
//             y: 20
//         }, {
//             name: '塔机/升降机',
//             y: 30
//         }, {
//             name: '深基坑/高支模',
//             y: 50
//         }]
//     }],
//     colors: ['#7386EE', '#F68A69', '#FBDFB1', '#7BD9F7']
// }, function(c) { // 图表初始化完毕后的会掉函数
//     // 环形图圆心
//     var centerY = c.series[0].center[1],
//         titleHeight = parseInt(c.title.styles.fontSize);
//     // 动态设置标题位置
//     c.setTitle({
//         y: centerY + titleHeight / 2
//     });
// });


// 人员概况
var dom = document.getElementById("memberChart");
var myChart = echarts.init(dom);
option = {
    backgroundColor: 'transparent',
    tooltip: {
        axisPointer: {
            type: 'shadow'
        }
    },
    grid: {
        top: '15%',
        right: '3%',
        left: '5%',
        bottom: '12%'
    },
    xAxis: [{
        type: 'category',
        data: ['环境', '人员', '塔吊', '升降机', '基坑支模'],
        axisLine: {
            lineStyle: {
                color: 'rgba(255,255,255,0.12)'
            }
        },
        axisLabel: {
            margin: 5,
            color: '#e2e9ff',
            textStyle: {
                fontSize: 14
            },
        },
    }],
    yAxis: [{
        axisLabel: {
            formatter: '{value}',
            color: '#e2e9ff',
        },
        axisLine: {
            show: false
        },
        splitLine: {
            lineStyle: {
                color: 'rgba(255,255,255,0.12)'
            }
        }
    }],
    series: [{
        type: 'bar',
        data: [30, 45, 77, 29, 56],
        barWidth: '20%',
        itemStyle: {
            normal: {
                color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [{
                    offset: 0,
                    color: 'rgba(232,230,189,1)' // 0% 处的颜色
                }, {
                    offset: 1,
                    color: 'rgba(68,133,193,1)' // 100% 处的颜色
                }], false),
                barBorderRadius: [30, 30, 0, 0],
                shadowColor: 'rgba(0,160,221,1)',
                shadowBlur: 4,
            }
        }
    }]
};
myChart.setOption(option);

// var chart = Highcharts.chart('hFcontainer', {
//     chart: {
//         type: 'areaspline',
//         backgroundColor: 'transparent',
//     },
//     title: {
//         text: '包含负值的面积图',
//         style: {
//             display: "none"
//         }
//     },
//     xAxis: {
//         categories: ['7.24', '7.25', '7.26', '7.27', '7.28', '7.29', '7.30'],
//         labels: {
//             rotation: 0, // 设置轴标签旋转角度
//             style: {
//                 color: "#fff"
//             }
//         },
//         lineColor: "#527dff",
//         color: '#FFFFFF',
//     },
//     yAxis: {
//         allowDecimals: false,
//         min: 0,
//         title: {
//             text: 'ug/m³',
//             style: {
//                 color: "#fff"
//             }
//         },
//         labels: {
//             style: {
//                 color: "#fff"
//             }
//         },
//         lineColor: "#56ABEC",
//         gridLineWidth: 0,
//         gridLineColor: '#444642'
//     },
//     credits: {
//         enabled: false
//     },
//     plotOptions: {
//         areaspline: {
//             fillColor: {
//                 linearGradient: {
//                     x1: 0,
//                     y1: 0,
//                     x2: 0,
//                     y2: 1
//                 },
//                 stops: [
//                     [0, "#374d90"],
//                     [1, "rgba(82,125,255,0)"]
//                 ]
//             },
//             marker: { // 点
//                 radius: 2,
//                 fillColor: "#fff",
//             },
//             lineWidth: 1,
//             states: {
//                 hover: {
//                     lineWidth: 2,
//                     marker: {
//                         radius: 1
//                     }
//                 }
//             },
//             threshold: null, //阀值
//             color: "#a8baff", //数据列线条颜色
//         }
//     },
//     tooltip: {
//         pointFormat: 'PM2.5：{point.y:,.0f}T'
//     },
//     series: [{
//         name: 'PM2.5',
//         data: [5, 3, 4, 5, 4, 5, 6]
//     }]
// });

// 质量整改率
var dom = document.getElementById("quality");
var myChart = echarts.init(dom);
option = {
    backgroundColor: 'transparent',
    grid: {
        y: '30',
        x: '10',
        x2: '10',
        y2: '0',
        containLabel: true
    },
    title: {
        text: null,
        x: 'center',
        y: 'top',
        itemGap: 20,
        textStyle: {
            color: '#000',
            fontFamily: '微软雅黑',
            fontSize: 18,
            fontWeight: 'bolder'
        }
    },
    tooltip: {
        trigger: 'item',
        formatter: "{b}: {d}%"
    },
    series: [{
            name: '质量整改率',
            center: ['center', 'center'],
            type: 'pie',
            radius: ['40%', '60%'],
            hoverAnimation: false,
            itemStyle: {
                normal: {
                    label: {
                        show: true,
                        distance: 0.7,
                        textStyle: { color: '#fff', fontSize: "10" },
                        formatter: '{b} {b|{d}%}',
                        rich: {
                            a: {
                                color: "#fff",
                            },
                            b: {
                                color: '#fff',
                            },
                        }
                    },
                },
            },

            data: [{
                    value: 6000,
                    name: '已整改',
                    itemStyle: {
                        color: new echarts.graphic.LinearGradient(0, 1, 0, 0, [{
                                offset: 1,
                                color: "#DAFCEE" // 0% 处的颜色
                            },
                            {
                                offset: 0,
                                color: "#67A2CA" // 100% 处的颜色
                            }
                        ], false),
                    },
                },
                {
                    value: 2000,
                    name: '未整改',
                    itemStyle: {
                        color: '#888f9b',

                    }
                },
            ]
        },
        {
            name: '质量整改率',
            center: ['center', 'center'],
            type: 'pie',
            radius: ['36%', '34%'],
            hoverAnimation: false,
            label: {
                normal: {
                    show: true,
                    position: 'center',
                    formatter: function(argument) {
                        var html;
                        html = '质量\r\n\r\n' + '整改率';
                        return html;
                    },
                    textStyle: {
                        fontSize: 12,
                        color: '#5C6498'
                    }
                }
            },
            data: [{
                value: 6000,
                name: '质量整改率',
                itemStyle: {
                    color: 'transparent'
                }
            }, ]
        }

    ]
};
myChart.setOption(option);

// 安全整改率
var dom = document.getElementById("security");
var myChart = echarts.init(dom);
option = {
    backgroundColor: 'transparent',
    grid: {
        y: '30',
        x: '10',
        x2: '10',
        y2: '0',
        containLabel: true
    },
    title: {
        text: null,
        x: 'center',
        y: 'top',
        itemGap: 20,
        textStyle: {
            color: '#000',
            fontFamily: '微软雅黑',
            fontSize: 18,
            fontWeight: 'bolder'
        }
    },
    tooltip: {
        trigger: 'item',
        formatter: "{b}: {d}%"
    },
    series: [{
            name: '安全整改率',
            center: ['center', 'center'],
            type: 'pie',
            radius: ['40%', '60%'],
            hoverAnimation: false,
            itemStyle: {
                normal: {
                    label: {
                        show: true,
                        distance: 0.7,
                        textStyle: { color: '#fff', fontSize: "10" },
                        formatter: '{b} {b|{d}%}',
                        rich: {
                            a: {
                                color: "#fff",
                            },
                            b: {
                                color: '#fff',
                            },
                        }
                    },
                },
            },

            data: [{
                    value: 6000,
                    name: '已整改',
                    itemStyle: {
                        color: new echarts.graphic.LinearGradient(0, 1, 0, 0, [{
                                offset: 1,
                                color: "#FEFCC9" // 0% 处的颜色
                            },
                            {
                                offset: 0,
                                color: "#F79472" // 100% 处的颜色
                            }
                        ], false),
                    },
                },
                {
                    value: 2000,
                    name: '未整改',
                    itemStyle: {
                        color: '#888f9b',

                    }
                },
            ]
        },
        {
            name: '安全整改率',
            center: ['center', 'center'],
            type: 'pie',
            radius: ['36%', '34%'],
            hoverAnimation: false,
            label: {
                normal: {
                    show: true,
                    position: 'center',
                    formatter: function(argument) {
                        var html;
                        html = '安全\r\n\r\n' + '整改率';
                        return html;
                    },
                    textStyle: {
                        fontSize: 12,
                        color: '#5C6498'
                    }
                }
            },
            data: [{
                value: 6000,
                name: '安全整改率',
                itemStyle: {
                    color: 'transparent'
                }
            }, ]
        }

    ]
};
myChart.setOption(option);

// 安全文明教育
var dom = document.getElementById("civilization");
var myChart = echarts.init(dom);
// 指定图表的配置项和数据
var option = {
    tooltip: {
        show: false
    },
    grid: {
        top: '5%',
        left: '5%',
        right: '5%',
        bottom: '10%',
    },
    xAxis: {
        data: ['今日', '历史'],
        offset: 1,
        axisTick: {
            show: false
        },
        axisLine: {
            show: false
        },
        axisLabel: {
            color: '#fff',
            fontSize: 14,
            fontWeight: 500
        }
    },
    yAxis: {
        min: 0,
        max: 100,
        splitLine: {
            show: false
        },
        axisTick: {
            show: false
        },
        axisLine: {
            show: false
        },
        axisLabel: {
            show: false
        }
    },
    series: [{
        type: 'bar',
        label: {
            show: true,
            position: 'top',
            padding: 0,
            color: '#fff',
            fontSize: 14,
            formatter: '{c}%'
        },
        itemStyle: {
            normal: {
                color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [{
                    offset: 0,
                    color: '#B2F1F6'
                }, {
                    offset: 1,
                    color: '#7586EE'
                }]),
                barBorderRadius: 7,
            },
        },
        barWidth: '40%',
        data: [70, 80],
        z: 10
    }, {
        type: 'bar',
        barGap: '-100%',
        itemStyle: {
            normal: {
                color: '#333969',
                barBorderRadius: 7,
            },
            barBorderRadius: 100,
        },
        barWidth: '40%',
        data: [100, 100, 100],
        z: 5
    }, {
        type: 'bar',
        barGap: '-100%',
        itemStyle: {
            color: '#333969',
            barBorderRadius: 7,
        },
        barWidth: '40%',
        data: [100, 100, 100],
        z: 5
    }],
    backgroundColor: "transparent",
};
myChart.setOption(option);

// 塔机监测
var dom = document.getElementById("monitor");
var myChart = echarts.init(dom);
option = {
    backgroundColor: 'transparent', //背景颜色
    tooltip: {
        show: true,
        formatter: "{a} <br/>{b} : {c}"
    },
    legend: {
        left: "center",
        textStyle: {
            "color": "#fff",
            "fontSize": 16
        },
        icon: "circle",
        top: "0",
        padding: [20, 20],
        itemGap: 40,
        data: ['正常', '异常', '掉线'],
        itemStyle: {
            colors: ['#7386EE', '#FF0000', '#7BD9F7'],
            fontWeight: 'normal'
        },
        textStyle: {
            color: '#e2e9ff'
        }
    },
    title: [{
        // left: 'center',
        left: '49%',
        top: '30%',
        textAlign: 'center',
        text: '6',
        textStyle: {
            fontSize: 16,
            fontWeight: 700,
            color: '#fff'
        },
        subtext: '塔吊',
        subtextStyle: {
            fontSize: 12,
            color: ['#fff']
        },
    }, {
        left: '49%',
        top: '75%',
        textAlign: 'center',
        text: '6',
        textStyle: {
            fontSize: 16,
            fontWeight: 700,
            color: '#fff'
        },
        subtext: '升降机',
        subtextStyle: {
            fontSize: 12,
            color: ['#fff']
        },
    }],
    series: [{
            name: '塔吊',
            type: 'pie',
            center: ['50%', '35%'],
            radius: [50, 70],
            data: [
                { value: 4, name: '正常' },
                { value: 1, name: '异常' },
                { value: 1, name: '掉线' }
            ],
            itemStyle: { //系列级个性化
                normal: {
                    color: function(params) {
                        var colorList = [
                            '#7386EE', '#FF0000', '#7BD9F7'
                        ];
                        return colorList[params.dataIndex]
                    },
                    labelLine: { //饼图不显示线条
                        length: 2,
                        show: true
                    },
                    label: { //饼图不显示文字
                        show: true,
                        distance: 0.7,
                        textStyle: { color: '#fff', fontSize: "10" },
                        formatter: '{b} : {c}台',
                    },
                }
            }
        },
        {
            name: '升降机',
            type: 'pie',
            center: ['50%', '80%'],
            radius: [50, 70],
            data: [
                { value: 3, name: '正常' },
                { value: 2, name: '异常' },
                { value: 1, name: '掉线' }
            ],
            itemStyle: { //系列级个性化
                normal: {
                    color: function(params) {
                        var colorList = [
                            '#7386EE', '#FF0000', '#7BD9F7'
                        ];
                        return colorList[params.dataIndex]
                    },
                    labelLine: { //饼图不显示线条
                        length: 2,
                        show: true
                    },
                    label: { //饼图不显示文字
                        show: true,
                        distance: 0.7,
                        textStyle: { color: '#fff', fontSize: "10" },
                        formatter: '{b} : {c}台',
                    },
                }
            }
        }
    ]
};
myChart.setOption(option);