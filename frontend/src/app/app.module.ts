import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';

import { HttpClientModule } from '@angular/common/http';
// import { MyComponentWrapperComponent} from './MyReactComponentWrapper'
import { APP_BASE_HREF, LocationStrategy, HashLocationStrategy, registerLocaleData } from '@angular/common';
import { FormsModule } from '@angular/forms';

// ant ui
import { NzButtonModule } from 'ng-zorro-antd/button';
import { NZ_I18N } from 'ng-zorro-antd/i18n';
import { en_US } from 'ng-zorro-antd/i18n';
import en from '@angular/common/locales/en';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';

import * as PlotlyJS from 'plotly.js-dist-min';
import { PlotlyModule } from 'angular-plotly.js';

import { AngularSlickgridModule } from 'angular-slickgrid';


PlotlyModule.plotlyjs = PlotlyJS;

import { NgZorroAntdModule} from './ng-zorro-antd.module';
import { CodeComponent } from './components/elements/code/code.component';
import { ExpanderComponent } from './components/elements/expander/expander.component';
import { EditableComponent } from './components/elements/editable/editable.component'
registerLocaleData(en);

// @dynamic
@NgModule({
  declarations: [
    AppComponent,
    CodeComponent,
    ExpanderComponent,
    EditableComponent,
    // MyComponentWrapperComponent
  ],
  imports: [
    AngularSlickgridModule.forRoot(),
    BrowserModule,
    AppRoutingModule,
    HttpClientModule,
    FormsModule,
    NzButtonModule,
    BrowserAnimationsModule,
    PlotlyModule,
    NgZorroAntdModule

  ],
  providers: [{ provide: APP_BASE_HREF, useValue: '/' },
  { provide: LocationStrategy, useClass: HashLocationStrategy },
  { provide: NZ_I18N, useValue: en_US },],
  bootstrap: [AppComponent]
})
export class AppModule { }
