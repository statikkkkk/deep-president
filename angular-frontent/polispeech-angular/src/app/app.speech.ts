import {
    Component,
    ElementRef,
    AfterViewInit,
    OnDestroy,
    ViewChild
} from '@angular/core';

import {
    QueryService
} from './../services/query.service';
import {
    HttpClient
} from '../services/httpclient.service';


import {Router} from '@angular/router';


const Highcharts = require('highcharts/highcharts.src');
import 'highcharts/adapters/standalone-framework.src';


@Component({
    selector: 'app-root',
    templateUrl: './app.speech.html',
    styleUrls: ['./app.component.css'],
    providers: [QueryService, HttpClient]
})


export class SpeechComponent {

    @ViewChild('chart') public chartEl: ElementRef;
    @ViewChild('chart2') public chartEl2: ElementRef;

    private _chart: any;
    private _chart2: any;


    private randomValue() {
        return Math.floor(Math.random() * 10) + 0;
    }


    public ngOnDestroy() {
        this._chart.destroy();

    }

    constructor(private queryService: QueryService, private router: Router) {
        this.check_val()
    }

    words: string[] = []
    polarity: any = {}
    type: number = 1
    get_color() {

    }

    public aftercall() {

        var words = this.words;
        var polarity = this.polarity;
        let opts: any = {
            title: {
                text: 'Polarity'
            },

            xAxis: {
                type: 'datetime',
                tickPixelInterval: 150
            },
            series: [{
                name: 'Sentiment Frequency',
                data: (function() {
                    // generate an array of random data
                    var data = [],
                        time = (new Date()).getTime(),
                        i;
                    console.log(polarity)
                    for (var i: any = -1 * Math.floor(words.length / 6.0); i <= 0; i += 1) {
                        var sum = 0
                        for (var j = 0; j < 6; j += 1) {
                            sum += polarity[words[6 * (i) + j]]
                        }

                        data.push({
                            x: time + i * 2000,
                            y: 0
                        });
                    }
                    return data;
                }())
            }]
        };
        if (this.chartEl && this.chartEl.nativeElement) {
            opts.chart = {
                type: 'spline',
                renderTo: this.chartEl.nativeElement
            };

            this._chart = new Highcharts.Chart(opts);
        }




        var words = this.words;
        var polarity = this.polarity;
        const me = this;
        var router = this.router;

        var i = 0
        setInterval(function() {

            if (me._chart) {

                var sum = 0
                for (var j = 0; j < 6; j += 1) {

                    if (polarity[words[6 * (i) + j]] != null) {

                        sum += polarity[words[6 * (i) + j]]
                    }
                }
                console.log(sum)

                me._chart['series'][0].addPoint([(new Date()).getTime(), sum], true, true);
                i = i + 1

                if(i*6>words.length){
                  router.navigateByUrl('/');
                }


            }
        }, 2000);
    }



    check_val() {
        this.queryService.checkSpeech().subscribe(
            res => {
                this.words = res.words.split(" ");
                this.polarity = res.word_polarity
                this.aftercall()
                
            }, err => {
                console.log(err)
                setTimeout(this.check_val(), 2000);
            })
    }

}