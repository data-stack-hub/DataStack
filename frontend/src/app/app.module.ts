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
import { NzSelectModule } from 'ng-zorro-antd/select';
import { NzCollapseModule } from 'ng-zorro-antd/collapse';
import { NzDividerModule } from 'ng-zorro-antd/divider';
import { NzListModule } from 'ng-zorro-antd/list';
registerLocaleData(en);

@NgModule({
  declarations: [
    AppComponent,
    // MyComponentWrapperComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    HttpClientModule,
    FormsModule,
    NzButtonModule,
    BrowserAnimationsModule,
    NzSelectModule,
    NzCollapseModule,
    NzDividerModule,
    NzListModule
  ],
  providers: [{ provide: APP_BASE_HREF, useValue: '/' },
  { provide: LocationStrategy, useClass: HashLocationStrategy },
  { provide: NZ_I18N, useValue: en_US },],
  bootstrap: [AppComponent]
})
export class AppModule { }
