import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { CreateStoryComponent } from './components/create-story/create-story.component';
import { EditStoryComponent } from './components/edit-story/edit-story.component';
import { FirstPageComponent } from './layouts/first-page/first-page.component';
import { HomeComponent } from './layouts/home/home.component';

const routes: Routes = [
  { path: '', component: FirstPageComponent },
  { path: 'home', component: HomeComponent },
  { path: 'write-new-story', component: CreateStoryComponent },
  { path: 'edit-story/:id', component: EditStoryComponent }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
