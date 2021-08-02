
Highcharts.chart('chart2', {
    chart: {
      backgroundColor:'#0000',
      height: 250,
        zoomType: 'xy'
    },
    
    navigation: {
buttonOptions: {
  enabled: false
  }
 },

        title: {
        text: 'Avg. RPM & Counter',
        style: {
                color: '#e6ffff',
                fontSize: '22px'
            
            }
    },
    xAxis: [{
         color:'red',
        categories: x_axis_data,
        crosshair: true
       
    }],
    yAxis: [{ gridLineWidth: false,

    // Primary yAxis

        labels: {
            gridLineWidth:false,
            format: '{value} rpm',
            style: {
                color: '#ffffff'
            }
        },
        title: {
            text: 'Avg. RPM',
            style: {
                color: '#ffffff'
            },

        },
        gridLineColor:'transparent'
    }, { // Secondary yAxis


        title: {
            text: 'Counter',
            style: {
                color: Highcharts.getOptions().colors[0]
            }
        },
        gridLineColor:'transparent',
        labels: {
            gridLineWidth: 0,
            format: '{value}',
            style: {
                color: Highcharts.getOptions().colors[0]
            }
        },
        opposite: true
    }],
    tooltip: {
        shared: true
    },




        plotOptions: {
        series: {
            animation: false,
            color: '#0086b3'
        }
    },
        legend: {
        
      itemStyle:{color: '#e6ffff'},
        
        
        backgroundColor:
            Highcharts.defaultOptions.legend.backgroundColor || // theme
            'transparent'
    },
    series: [{
        name: 'Counter',
        type: 'column',
        yAxis: 1,
         data: bar_graph_y_axis,


    }, {
      color: '#ffffff',
        name: 'Avg. RPM',
        type: 'spline',
        data: line_graph_y_axis,
                tooltip: {
            valueSuffix: 'rpm'
        }
    }]
});