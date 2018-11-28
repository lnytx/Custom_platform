<!--将时间戳转换成日期格式-->

function timestampToTime(timestamp) {
        var date = new Date(timestamp * 1000);//时间戳为10位需*1000，时间戳为13位的话不需乘1000
        Y = date.getFullYear() + '-';
        M = (date.getMonth()+1 < 10 ? '0'+(date.getMonth()+1) : date.getMonth()+1) + '-';
        D = date.getDate() + ' ';
        h = date.getHours() + ':';
        m = date.getMinutes() + ':';
        s = date.getSeconds();
        return Y+M+D+h+m+s;
    }
console.log("时间转换",timestampToTime(1517973856))

$(function(){
var data = [[1517976076,856],
                    [1517976016,781],
                    [1517975956,744],
                    [1517975896,732],
                    [1517975836,775],
                    [1517975836,776],
                    [1517973976,777],
                    [1517973916,778],
                    [1517973856,779],
                    [1517975836,780],
                    [1517975836,781],
                    ];


	 var title = {
      text: '城市平均气温'   
   };
   var subtitle = {
      text: 'Source: runoob.com'
   };
   var xAxis = {
     type: 'datetime',
      dateTimeLabelFormats: { // don't display the dummy year
         month: '%e. %b',
         year: '%b'
         }
   };
   var yAxis = {
      title: {
         text: 'Temperature (\xB0C)'
      },
      plotLines: [{
         value: 0,
         width: 1,
         color: '#808080'
      }]
   };   

   var tooltip = {
     headerFormat: '<span style="color:{series.color};"></span><span>{point.key}</span>',
                    pointFormat: '<table>'+
                                 '<tr><td style="color:{series.color};">{series.name}:</td>' +
                                 '<td><b>{point.y:.0f}</b></td></tr>',
                    footerFormat:'</table>',
                    shared: true,
                    useHTML: true,
                    xDateFormat:'%Y-%m-%d %H:%M:%S '
   }

   var legend = {
      layout: 'vertical',
      align: 'right',
      verticalAlign: 'middle',
      borderWidth: 0
   };

   var series =  [
      {
         name: 'aaaa',
         data:data
      }
   ];

   var json = {};

   json.title = title;
   json.subtitle = subtitle;
   json.xAxis = xAxis;
   json.yAxis = yAxis;
   json.tooltip = tooltip;
   json.legend = legend;
   json.series = series;

   $('#container').highcharts(json);

});
