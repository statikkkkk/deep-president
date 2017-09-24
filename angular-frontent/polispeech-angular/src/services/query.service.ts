import {Injectable} from '@angular/core'
import {Response} from '@angular/http'
import { config } from '../app.config'
import { HttpClient } from './httpclient.service';
import 'rxjs/add/operator/map'
import 'rxjs/add/operator/timeout'

@Injectable()
export class QueryService{
	constructor(private http: HttpClient){}
	checkSpeech(){
		return this.http.get(config.URI+'/get_current_speech').timeout(3000).map(res => res.json());
	}
}