<template>
  <el-table
    :data="pageData"
    ref="goodsTable"
    size="small"
    v-loading="loading"
    @selection-change="handleSelectionChange"
    :row-key="getRowKeys"
  >
    <el-table-column type="selection" :reserve-selection="true" width="50" prop="id"></el-table-column>
    <el-table-column label="编号" prop="goodsCode" width="130"></el-table-column>
  </el-table>
</template>
<script>
export default {
  name: 'copy',  
  filters: {
    statusFilter(status) {
      if (status !== "" && status !== null) {
        const statusMap = {
          "1": "待审批",
          "2": "销售中",
          "3": "已拒批",
          "4": "已停售"
        };
        return statusMap[status];
      }
      return "—";
    }
  },
  data() {
    return {
      pageData: [{goodsCode:'asd'},{goodsCode:'asd'},{goodsCode:'asd'},{goodsCode:'asd'},{goodsCode:'asd'},{goodsCode:'asd'},{goodsCode:'asd'},{goodsCode:'asd'},{goodsCode:'asd'},{goodsCode:'asd'},{goodsCode:'asd'}],
      loading: false,
      // 获取row的key值
      getRowKeys(row) {
        return row.id;
      },
      selectedData: []
    };
  },
  methods: {
    handleSelectionChange(rows) {
      this.selectedData = [];
      if (rows) {
        rows.forEach(row => {
          if (row) {
            this.selectedData.push(row.id);
          }
        });
      }
      console.log(this.selectedData);
    }
  }
};
</script>