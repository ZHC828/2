from django.shortcuts import render,redirect
from .models import Topic,Entry
from django.contrib.auth.decorators import login_required
from .forms import TopicForm,EntryForm
from django.http import Http404
# Create your views here.
def index(request):
    """主页"""
    return render(request,'learning_logs/index.html')
@login_required
def topics(request):
    """显示主题"""
    topics = Topic.objects.filter(owner = request.user).order_by('data_added')
    context = {'topics':topics}
    return  render(request,'learning_logs/topics.html',context)
@login_required
def topic(request,topic_id):
    topic= Topic.objects.get(id = topic_id)
    if topic.owner != request.user:
        raise Http404
    entries =topic.entry_set.order_by('-data_added')
    context = {'topic':topic,'entries':entries}
    return render(request, 'learning_logs/topic.html',context)
@login_required
def new_topic (request):
    #添加新主题
    if request.method != 'POST':
        #创建新表单
        form = TopicForm()

    else:
    #POST提交的数据，数据处理
        form = TopicForm(data=request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return redirect('learning_logs:topics')
    #指出错误，空表单或无效
    context = {'form':form}
    return render(request,'learning_logs/new_topic.html',context)
@login_required
def new_entry(request,topic_id):
    #特定主题下添加新条目
    topic = Topic.objects.get(id=topic_id)
    if request.method != "POST":
        form = EntryForm()

    else:
        #数据处理
        form = EntryForm(data = request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return redirect('learning_logs:topic', topic_id = topic_id)
    #显示空表单
    context = {'topic':topic,'form':form}
    return render(request,'learning_logs/new_entry.html',context)
@login_required
def edit_entry(request,entry_id):
    entry = Entry.objects.get(id = entry_id)
    topic = entry.topic
    if topic.owner != request.user :
        raise Http404

    if request.method != 'POST':
        form = EntryForm(instance= entry)

    else:
        form = EntryForm( instance= entry ,data = request.POST )
        if form.is_valid():
            form.save()
            return redirect('learning_logs:topic',topic_id = topic.id)

    context = {'entry': entry,'topic':topic,'form':form}
    return render(request,'learning_logs/edit_entry.html',context)
