import { Component } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { Category } from 'src/app/models/category';
import { Story } from 'src/app/models/story';
import { StoryService } from 'src/app/services/story.service';

@Component({
  selector: 'app-edit-story',
  templateUrl: './edit-story.component.html',
  styleUrls: ['./edit-story.component.css']
})
export class EditStoryComponent {
  storyForm!: FormGroup;
  categories!: Category[];
  story: Story = new Story();

  constructor(private formBuilder: FormBuilder,
              private storyService: StoryService,
              private router: Router,
              private route: ActivatedRoute) { }

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

  this.route.paramMap.subscribe(params => {
    let tmp: any = params.get('id');
    this.storyService.getStory(tmp).subscribe(res => {
      this.story = res['story'];
      console.log(this.story)
      let formData = {
        title: res['story']['title'],
        text: res['story']['text'],
        category: res['story']['category']['id']
      }
      this.storyForm.setValue(formData);
    })
  });
}

get f() { return this.storyForm.controls; }

onSubmit() {
    if (this.storyForm.invalid) {
      return;
  }

  this.story.title = this.f["title"].value;
  this.story.text = this.f["text"].value;
  this.story.category.id = this.f["category"].value;

  this.storyService.updateStory(this.story).subscribe({
                        error: (e) => console.error(e),
                        complete: () => {
                          console.info('complete')
                          this.router.navigateByUrl('/home');
                      }  
                      })
}

}
