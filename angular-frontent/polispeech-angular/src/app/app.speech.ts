import { Component } from '@angular/core';
import {QueryService} from './../services/query.service';
import { HttpClient } from '../services/httpclient.service';


@Component({
  selector: 'app-root',
  templateUrl: './app.speech.html',
  styleUrls: ['./app.component.css'], 
  providers: [QueryService, HttpClient]
})
export class SpeechComponent {

	current_text:string = ""
	constructor(private queryService: QueryService){
    	queryService.checkSpeech().subscribe(
    	res => {
    		if(this.current_text != "" && res.text() != this.current_text){
    			console.log("UPDATED STRINGGGG")
    		}
    		this.current_text = res.text()
    	},err => { 
    		console.log(err)
    	})
    }
}
