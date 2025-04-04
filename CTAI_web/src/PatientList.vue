<template>
  <div id="patient-list">
    <el-dialog title="肿瘤辅助诊断系统使用须知" :visible.sync="centerDialogVisible" width="65%" :before-close="handleClose">
      <el-steps :active="3" finish-status="process">
        <el-step title="步骤1" style="width:280px;padding-left: 50px">
          <template slot="description">
            <p style="font-size: 16px">选择患者进行诊断</p>
            <br>
            <br>
          </template>
        </el-step>
        <el-step title="步骤2" style="width:260px;margin-left:-5px;">
          <template slot="description">
            <p>查看患者CT图像</p>
            <p>进行肿瘤区域识别</p>
            <p>获取肿瘤区域特征</p>
          </template>
        </el-step>
        <el-step title="步骤3" style="width:260px;margin-left:-5px;">
          <template slot="description">
            <div>
              <p>跟踪患者历史诊断记录</p>
              <p>分析肿瘤发展趋势</p>
              <br>
            </div>
          </template>
        </el-step>
      </el-steps>
      <span slot="footer" class="dialog-footer">
        <el-button type="primary" @click="centerDialogVisible = false">开始使用</el-button>
      </span>
    </el-dialog>

    <div class="container">
      <h1 class="page-title">患者列表</h1>
      <div class="search-box">
        <el-input placeholder="请输入患者姓名或ID搜索" v-model="searchQuery" class="search-input" prefix-icon="el-icon-search">
        </el-input>
        <div>
          <el-button type="primary" icon="el-icon-plus" @click="addNewPatient">添加患者</el-button>
          <el-button type="danger" icon="el-icon-refresh" @click="resetPatientData">重置数据</el-button>
        </div>
      </div>

      <el-table :data="filteredPatients.slice((currentPage - 1) * pageSize, currentPage * pageSize)" style="width: 100%"
        :default-sort="{ prop: 'id', order: 'ascending' }">
        <el-table-column prop="id" label="患者ID" sortable width="150"></el-table-column>
        <el-table-column prop="name" label="姓名" sortable width="150"></el-table-column>
        <el-table-column prop="gender" label="性别" width="100"></el-table-column>
        <el-table-column prop="age" label="年龄" sortable width="100"></el-table-column>
        <el-table-column prop="phone" label="联系电话" width="180"></el-table-column>
        <el-table-column prop="department" label="科室" width="150"></el-table-column>
        <el-table-column prop="lastDiagnosis" label="最近诊断日期" sortable width="180"></el-table-column>
        <el-table-column label="操作" width="200">
          <template slot-scope="scope">
            <el-button size="mini" type="primary" @click.stop="viewPatient(scope.row)">查看</el-button>
            <el-button size="mini" type="info" @click.stop="viewHistory(scope.row)">就诊记录</el-button>
          </template>
        </el-table-column>
      </el-table>

      <!-- 分页组件 -->
      <el-pagination @size-change="handleSizeChange" @current-change="handleCurrentChange" :current-page="currentPage"
        :page-sizes="[5, 10, 15, 20]" :page-size="pageSize" layout="total, sizes, prev, pager, next, jumper"
        :total="filteredPatients.length" class="pagination">
      </el-pagination>
    </div>

    <!-- 添加新患者的对话框 -->
    <el-dialog title="添加新患者" :visible.sync="dialogVisible" width="40%">
      <el-form :model="newPatient" label-width="80px">
        <el-form-item label="姓名">
          <el-input v-model="newPatient.name"></el-input>
        </el-form-item>
        <el-form-item label="性别">
          <el-select v-model="newPatient.gender" placeholder="请选择性别">
            <el-option label="男" value="男"></el-option>
            <el-option label="女" value="女"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="年龄">
          <el-input-number v-model="newPatient.age" :min="0" :max="120"></el-input-number>
        </el-form-item>
        <el-form-item label="电话">
          <el-input v-model="newPatient.phone"></el-input>
        </el-form-item>
        <el-form-item label="科室">
          <el-input v-model="newPatient.department"></el-input>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="saveNewPatient">保存</el-button>
      </span>
    </el-dialog>

    <!-- 重置数据确认对话框 -->
    <el-dialog title="确认重置" :visible.sync="resetDialogVisible" width="30%" center>
      <span>重置将删除所有新添加的患者，确定要重置数据吗？</span>
      <span slot="footer" class="dialog-footer">
        <el-button @click="resetDialogVisible = false">取消</el-button>
        <el-button type="danger" @click="confirmReset">确定重置</el-button>
      </span>
    </el-dialog>

  </div>
</template>

<script>
export default {
  name: "PatientList",
  data() {
    return {
      centerDialogVisible: false,
      dialogVisible: false,
      resetDialogVisible: false,
      searchQuery: '',
      currentPage: 1,
      pageSize: 10,
      defaultPatients: [
        {
          id: '20190001',
          name: '李明',
          gender: '男',
          age: 29,
          phone: '13220986785',
          department: '肛肠科',
          lastDiagnosis: '2025-01-15'
        },
        {
          id: '20190002',
          name: '王芳',
          gender: '女',
          age: 45,
          phone: '13587654321',
          department: '肛肠科',
          lastDiagnosis: '2025-01-18'
        },
        {
          id: '20190003',
          name: '张伟',
          gender: '男',
          age: 52,
          phone: '13898765432',
          department: '肛肠科',
          lastDiagnosis: '2025-01-10'
        },
        {
          id: '20190004',
          name: '刘娜',
          gender: '女',
          age: 38,
          phone: '13776543210',
          department: '肛肠科',
          lastDiagnosis: '2025-01-20'
        },
        {
          id: '20190005',
          name: '陈强',
          gender: '男',
          age: 61,
          phone: '13912345678',
          department: '肛肠科',
          lastDiagnosis: '2025-01-12'
        },
        {
          id: '20190006',
          name: '赵丽',
          gender: '女',
          age: 42,
          phone: '13766667777',
          department: '肛肠科',
          lastDiagnosis: '2025-02-05'
        },
        {
          id: '20190007',
          name: '黄建国',
          gender: '男',
          age: 57,
          phone: '13888889999',
          department: '肛肠科',
          lastDiagnosis: '2025-02-08'
        },
        {
          id: '20190008',
          name: '林小华',
          gender: '女',
          age: 36,
          phone: '13755556666',
          department: '肛肠科',
          lastDiagnosis: '2025-02-12'
        },
        {
          id: '20190009',
          name: '孙明亮',
          gender: '男',
          age: 48,
          phone: '13744445555',
          department: '肛肠科',
          lastDiagnosis: '2025-02-15'
        },
        {
          id: '20190010',
          name: '杨文静',
          gender: '女',
          age: 39,
          phone: '13733334444',
          department: '肛肠科',
          lastDiagnosis: '2025-02-18'
        },
        {
          id: '20190011',
          name: '周建军',
          gender: '男',
          age: 53,
          phone: '13722223333',
          department: '肛肠科',
          lastDiagnosis: '2025-03-01'
        },
        {
          id: '20190012',
          name: '吴桂英',
          gender: '女',
          age: 47,
          phone: '13711112222',
          department: '肛肠科',
          lastDiagnosis: '2025-03-05'
        },
        {
          id: '20190013',
          name: '郑文达',
          gender: '男',
          age: 64,
          phone: '13700001111',
          department: '肛肠科',
          lastDiagnosis: '2025-03-08'
        },
        {
          id: '20190014',
          name: '马丽丽',
          gender: '女',
          age: 34,
          phone: '13699998888',
          department: '肛肠科',
          lastDiagnosis: '2025-03-12'
        },
        {
          id: '20190015',
          name: '冯志强',
          gender: '男',
          age: 59,
          phone: '13688887777',
          department: '肛肠科',
          lastDiagnosis: '2025-03-15'
        }
      ],
      patients: [],
      newPatient: {
        name: '',
        gender: '男',
        age: 30,
        phone: '',
        department: '肛肠科'
      }
    };
  },
  computed: {
    filteredPatients() {
      const query = this.searchQuery.toLowerCase();
      return this.patients.filter(patient => {
        return patient.name.toLowerCase().includes(query) ||
          patient.id.toLowerCase().includes(query);
      });
    }
  },
  created() {
    // 从localStorage获取患者数据
    const storedPatients = localStorage.getItem('patientList');
    if (storedPatients) {
      this.patients = JSON.parse(storedPatients);
    } else {
      // 首次加载时，将默认患者列表保存到localStorage
      localStorage.setItem('patientList', JSON.stringify(this.defaultPatients));
      this.patients = this.defaultPatients;
    }

    // 确保弹窗不显示
    localStorage.setItem('hideWelcomeDialog', 'true');
  },
  methods: {
    handleClose(done) {
      this.$confirm('确认关闭提示信息？')
        .then(_ => {
          done();
        })
        .catch(_ => { });
    },
    handleRowClick(row) {
      this.viewPatient(row);
    },
    viewPatient(patient) {
      console.log('正在查看患者:', patient.id);
      // 将当前选中的患者信息保存到localStorage
      localStorage.setItem('currentPatient', JSON.stringify(patient));

      // 导航到诊断页面，传递患者ID
      this.$router.push(`/patient/${patient.id}`);

      // 确保弹窗不会显示
      localStorage.setItem('hideWelcomeDialog', 'true');
    },
    viewHistory(patient) {
      console.log('正在查看历史记录:', patient.id);
      // 导航到患者历史记录页面，使用完整路径
      localStorage.setItem('currentPatient', JSON.stringify(patient));

      // 使用两种方式尝试跳转
      try {
        this.$router.push(`/patient/${patient.id}/trend`);
      } catch (error) {
        console.error('路由跳转失败，尝试替代方案', error);
        // 如果上面的方式失败，尝试使用对象形式
        this.$router.push({
          path: `/patient/${patient.id}/history`
        });
      }
    },
    handleSizeChange(val) {
      this.pageSize = val;
    },
    handleCurrentChange(val) {
      this.currentPage = val;
    },
    addNewPatient() {
      this.dialogVisible = true;
      this.newPatient = {
        name: '',
        gender: '男',
        age: 30,
        phone: '',
        department: '肛肠科'
      };
    },
    saveNewPatient() {
      // 检查必填字段
      if (!this.newPatient.name) {
        this.$message.error('请输入患者姓名');
        return;
      }
      
      if (!this.newPatient.phone) {
        this.$message.error('请输入患者电话');
        return;
      }
      
      // 生成新ID (简单实现，实际应用中可能需要后端生成)
      const lastId = parseInt(this.patients[this.patients.length - 1].id);
      const newId = (lastId + 1).toString().padStart(8, '0');
      
      // 生成当前日期作为最近诊断日期 (2025年格式)
      const today = new Date();
      const year = 2025;
      const month = (today.getMonth() + 1).toString().padStart(2, '0');
      const day = today.getDate().toString().padStart(2, '0');
      const diagnosisDate = `${year}-${month}-${day}`;
      
      const patient = {
        id: newId,
        name: this.newPatient.name,
        gender: this.newPatient.gender,
        age: this.newPatient.age,
        phone: this.newPatient.phone,
        department: this.newPatient.department,
        lastDiagnosis: diagnosisDate
      };
      
      this.patients.push(patient);
      
      // 保存到localStorage
      localStorage.setItem('patientList', JSON.stringify(this.patients));
      
      // 为新患者清除历史记录标记，确保不会显示伪造的历史记录
      localStorage.removeItem(`patient_${newId}_hasUploaded`);
      
      // 获取现有历史记录数据
      const allHistory = JSON.parse(localStorage.getItem('patientHistoryRecords')) || {};
      
      // 确保新添加的患者没有历史记录
      if (allHistory[newId]) {
        delete allHistory[newId];
        localStorage.setItem('patientHistoryRecords', JSON.stringify(allHistory));
      }
      
      this.dialogVisible = false;
      
      this.$message({
        message: '新患者添加成功！',
        type: 'success'
      });
    },
    resetPatientData() {
      this.resetDialogVisible = true;
    },
    confirmReset() {
      // 创建一个深拷贝以避免引用问题
      this.patients = JSON.parse(JSON.stringify(this.defaultPatients));
      localStorage.setItem('patientList', JSON.stringify(this.patients));
      
      // 同时清除历史记录数据
      localStorage.removeItem('patientHistoryRecords');
      
      // 清除所有患者的上传记录标记
      for (const patient of this.patients) {
        localStorage.removeItem(`patient_${patient.id}_hasUploaded`);
        localStorage.removeItem(`patient_${patient.id}_area`);
        localStorage.removeItem(`patient_${patient.id}_perimeter`);
      }
      
      this.resetDialogVisible = false;
      
      // 重置当前页面到第一页
      this.currentPage = 1;
      
      this.$message({
        message: '数据重置成功！',
        type: 'success'
      });
    },
    handleSelect(patient) {
      // 将当前选中的患者信息保存到localStorage
      localStorage.setItem('currentPatient', JSON.stringify(patient));

      // 导航到诊断页面，传递患者ID
      this.$router.push({
        name: 'diagnosis',
        params: { id: patient.id }
      });

      // 确保弹窗不会显示
      if (localStorage.getItem('hideWelcomeDialog') !== 'true') {
        localStorage.setItem('hideWelcomeDialog', 'true');
      }
    }
  }
};
</script>

<style scoped>
.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.page-title {
  color: #17b3a3;
  text-align: center;
  margin-bottom: 30px;
  font-weight: 500;
}

.search-box {
  display: flex;
  justify-content: space-between;
  margin-bottom: 20px;
}

.search-input {
  width: 300px;
}

.pagination {
  margin-top: 20px;
  text-align: right;
}

.el-table {
  margin-top: 20px;
  border-radius: 4px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.el-table .el-table__row:hover {
  cursor: pointer;
}
</style>