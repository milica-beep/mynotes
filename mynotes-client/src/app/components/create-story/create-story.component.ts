import { Component } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { StoryService } from 'src/app/services/story.service';
import { Category } from 'src/app/models/category'

@Component({
  selector: 'app-create-story',
  templateUrl: './create-story.component.html',
  styleUrls: ['./create-story.component.css']
})
export class CreateStoryComponent {
  storyForm!: FormGroup;
  categories!: Category[];

  constructor(private formBuilder: FormBuilder,
              private storyService: StoryService,
              private router: Router) { }

ngOnInit(): void {
  this.storyForm = this.formBuilder.group({
    title: ['', Validators.required],
    text: ['', Validators.required],
    category: ['', Validators.required],
  });

  this.storyService.getCategories().subscribe(res => {
    console.log(res);
    this.categories = res['categories'];
  })
}

get f() { return this.storyForm.controls; }

onSubmit() {
    if (this.storyForm.invalid) {
      return;
  }

  let new_story =
  {
    "title": this.f["title"].value,
    "text": this.f["text"].value,
    "category": this.f["category"].value
  }

  this.storyService.createStory(new_story).subscribe({
                        error: (e) => console.error(e),
                        complete: () => {
                          console.info('complete')
                          this.router.navigateByUrl('/home');
                      }  
                      })
}

}
