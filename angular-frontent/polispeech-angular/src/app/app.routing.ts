import {ModuleWithProviders} from '@angular/core'
import {Routes, RouterModule} from '@angular/router'

import {SpeechComponent} from './app.speech'
import {PendingComponent} from './pending.component'


const appRoutes: Routes = [
	{path: "", component: PendingComponent},
	{path: "speech", component: SpeechComponent},
	
]

export const routing: ModuleWithProviders = RouterModule.forRoot(appRoutes)