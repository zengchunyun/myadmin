/**
 * Created by zengchunyun on 16/5/3.
 */
$(function () {

            Highcharts.getOptions().plotOptions.pie.colors = (function () {
                var colors = [],
                    base = Highcharts.getOptions().colors[0],
                    i;

                for (i = 0; i < 10; i += 1) {
                    colors.push(Highcharts.Color(base).brighten((i - 3) / 7).get());
                }
                return colors;
            }());
            $('#container').highcharts({
                chart: {
                    plotBackgroundColor: null,
                    plotBorderWidth: null,
                    plotShadow: false,
                    type: 'pie'
                },
                title: {
                    text: 'Operation System'
                },
                tooltip: {
                    pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>'
                },
                plotOptions: {
                    pie: {
                        allowPointSelect: true,
                        cursor: 'pointer',
                        dataLabels: {
                            enabled: true,
                            format: '<b>{point.name}</b>: {point.percentage:.1f} %',
                            style: {
                                color: (Highcharts.theme && Highcharts.theme.contrastTextColor) || 'black'
                            }
                        }
                    }
                },
                series: [{
                    name: 'Brands',
                    data: [
                        { name: 'Centos', y: 56.33 },
                        { name: 'Suse', y: 24.03 },
                        { name: 'Debian', y: 10.38 },
                        { name: 'Oracle', y: 4.77 },
                        { name: 'Ubuntu', y: 0.91 },
                        { name: 'Free BSD', y: 0.2 }
                    ]
                }]
            });
        });