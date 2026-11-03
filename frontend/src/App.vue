<template>
  <h1 class="head">111111</h1>
  <div class="bg"></div>
  <div style="margin-left: 5%;">
    <el-input clearable v-model="data.title" 
      placeholder="请输入书名查询"  style="width: 30%; 
      --el-text-color-placeholder: #a8abb2;
      --el-input-text-color: #a8abb2";
      @keyup.enter="load">
    </el-input>
    <el-input clearable v-model="data.author" 
      placeholder="请输入作者查询"  style="width: 30%; 
      --el-text-color-placeholder: #a8abb2;
      --el-input-text-color: #a8abb2;
      margin:0 2%;"
      @keyup.enter="load">
    </el-input>
    <el-button type="info" @click="load" >搜索</el-button>
    <el-button type="success" @click="handle_add()">新增图书</el-button>
  </div>

  <div style="margin: 3%;">
    <el-pagination
      background
      :hide-on-single-page="value"
      layout="prev, pager, next, total"
      @current-change="load"
      :total="data.total"
      v-model:current-page="data.page"
      v-model:page-size="data.pageSize"
      style="--el-pagination-button-color: black"
    />
  </div>

  <el-table class="my-table" :data="data.tableData" style="width: 100%; margin: 10px auto">
    <el-table-column prop="title" label="Title" width="150px"/>
    <el-table-column prop="author" label="Author" width="150px"/>
    <el-table-column prop="ISBN" label="ISBN"/>
    <el-table-column prop="publisher" label="Publisher"/>
    <el-table-column prop="publish_date" label="Publish Date" width="150px"/>
    <el-table-column prop="category" label="Category" width="120px"/>
    <el-table-column prop="price" label="Price" width="70px"/>
    <el-table-column prop="stock" label="Stock" width="70px"/> 
    <el-table-column prop="location" label="Location" width="150px"/>
    <el-table-column label="Opreator">
      <template #default="scope">
        <el-button type="primary" @click="handle_edit(scope.row)">编辑</el-button>
        <el-button type="danger" @click="handle_del(scope.row.id)">删除</el-button>
      </template>
    </el-table-column>
  </el-table>

  <el-dialog class="my-dialog" v-model="DialogVisible" title="新增图书" width="500px" :close-on-press-escape="true" :show-close="true" >
    <el-form ref="formRef" :model="data.form" label-width="80px"> 
      <el-form-item label="图书名称">
        <el-input v-model="data.form.title" placeholder="请输入图书名称"></el-input>
      </el-form-item>
      <el-form-item label="作者">
        <el-input v-model="data.form.author" placeholder="请输入作者名称"></el-input>
      </el-form-item>
      <el-form-item label="ISBN">
        <el-input v-model="data.form.ISBN" placeholder="请输入ISBN"></el-input>
      </el-form-item>
      <el-form-item label="出版社">
        <el-input v-model="data.form.publisher" placeholder="请输入出版社"></el-input>
      </el-form-item>
      <el-form-item label="出版日期">
        <el-date-picker popper-class="my-date-picker" v-model="data.form.publish_date" type="date" placeholder="请选择出版日期">
        </el-date-picker>
      </el-form-item> 
      <el-form-item label="作品分类">
        <el-input v-model="data.form.category" placeholder="请输入作品分类"></el-input>
      </el-form-item>
      <el-form-item label="图书价格">
        <el-input v-model="data.form.price" placeholder="请输入图书价格"></el-input>
      </el-form-item>
      <el-form-item label="收藏位置">
        <el-input v-model="data.form.location" placeholder="请输入收藏位置"></el-input>
      </el-form-item>
      <el-form-item label="库存数量">
        <el-input v-model="data.form.stock" placeholder="请输入库存数量"></el-input>
      </el-form-item>
    </el-form>

    <template #footer>
      <el-button @click="DialogVisible = false">取消</el-button>
      <el-button type="primary" @click="save">确定</el-button>
    </template>
  </el-dialog>

</template>

<style scoped>
  .head {
    text-align: center; 
    font-size: 40px; 
    font-weight: 500; 
    font-family: 'Courier New', Courier, monospace; 
    margin-top: 7%;
  }

  .bg {
    position: fixed;               
    inset: 0;                      
    background: url("@/assets/bg1.jpg");  /* 背景图地址；@ 是 src 目录的别名，引号内不能有空格 */
    background-size: repeat;        
    background-position: center;   
    z-index: -1;                  
  }

  /* ===== 遮罩层：盖在背景图上，把它整体压暗 ===== */
  .bg::after {
    content: "";                   /* 伪元素必须写 content 才会被渲染，空字符串即可 */
    position: absolute;            /* 相对 .bg 定位（.bg 是 fixed，正好当它的定位父级），所以遮罩只盖背景区域 */
    inset: 0;                      /* 四边贴满 .bg，刚好盖住整张背景图 */
    background: rgba(0, 0, 0, 0.7); /* 纯黑 + 0.8 不透明度 = 只剩 20% 亮度。调到 0.5 会亮些，0.9 几乎全黑 */
  }

  /* ===== 表格透明化：覆盖 Element Plus 自己的 CSS 变量 ===== */
  .my-table {
    --el-table-text-color: rgba(255, 255, 255, 0.85);
    --el-table-bg-color: rgba(255, 255, 255, 0.55);          /* 表格整体底色：55% 不透明的白，背景图能透过来 */
    --el-table-tr-bg-color: transparent;                     /* 每一行 <tr> 的底色：全透明，否则行会把表格底色盖住 */
    --el-table-header-bg-color: rgba(255, 255, 255, 0.35);   /* 表头 <th> 的底色：比表体淡一点，做出层次 */
    --el-table-row-hover-bg-color: rgba(255, 255, 255, 0.75);/* 鼠标悬停时整行的底色：比常态更亮，作为交互反馈 */
    --el-table-border-color: rgba(0, 0, 0, 0.7);            /* 单元格边框线颜色：淡黑，在半透明底上不刺眼 */
    background-color: transparent; /* 表格根元素自身背景：透明。注意它会盖掉上面的 --el-table-bg-color（优先级更高） */
    backdrop-filter: blur(10px);   /* 毛玻璃：把表格背后的画面模糊掉，文字更清晰（浏览器需支持） */
    border-radius: 8px;            /* 表格四个角变圆 */
    overflow: hidden;              /* 裁掉溢出圆角的部分，否则表头的直角会从圆角里顶出来 */
    width: fit-content;            /* 覆盖 Element Plus 默认的 width:100%，让表格宽度收缩到内容宽度 */
  }

</style>

<style>
  .my-dialog{
    --el-text-color-primary: #303133;
    --el-text-color-regular: #606266;
    --el-text-color-secondary: #909399; 
    --el-text-color-placeholder: #C0C4CC;
  }

  .my-date-picker{
    --el-text-color-primary: #303133;
    --el-text-color-regular: #606266;
    --el-text-color-secondary: #909399;
  }
</style>

<script setup>
import {reactive} from 'vue'
import { ref } from 'vue'
import axios from 'axios'
import { ElMessage } from 'element-plus'

const value = ref(true)
const DialogVisible = ref(false)
const formRef = ref(null)

const data = reactive({
  title: "",
  author: "",
  page: 1,
  pageSize: 5,
  total: 0,
  tableData: [],
  form: {}
})
const load = () =>{
  axios.get('/api' + '/book/selectPage',{
    params: {
      title: data.title,
      author: data.author,
      page: data.page,
      pageSize: data.pageSize,
    }
  }).then(res => {
    data.tableData = res.data.message
    data.total = res.data.total
  })
  console.log(data.total)
}

const handle_add = () =>{
  console.log("新增操作")
  DialogVisible.value = true
  data.form = {} // 清空表单数据
}

const add = () =>{
  axios.post('/api' + '/book/', data.form).then(res => {
    if(res.status === 200){
      ElMessage.success("success")
    }else{
      ElMessage.error("error")
    }
  })
  load()
}
const handle_edit = (row) =>{
  console.log("编辑操作")
  DialogVisible.value = true
  data.form = JSON.parse(JSON.stringify(row))
}

const update = () =>{
  axios.put('/api' + '/book/', data.form).then(res => {
    if(res.status === 200){
      ElMessage.success("success")
    }else{
      ElMessage.error("error")
    }
    load()
  })
}

const handle_del = (id) =>{
  console.log("删除操作")
  axios.delete('/api' + '/book/',{ params: { id } }).then(res => {
    if(res.status === 200){
      ElMessage.success("success")
    }else{
      ElMessage.error("error")
    }
    load()
  })
}

const save = () =>{ 
  DialogVisible.value = false
  formRef.value.validate(valid => {
    if (valid) {
      if(data.form.id){
        update()
      }else{
        add()
      }
    }
  })
}
  
load()
</script>

