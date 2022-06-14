<template>
<div class="wrapper">
  <form id="search">
    Search <input name="query" v-model="searchQuery">
  </form>
  <div id="grid-template">
        <select v-model="rowsPerPage">
  <option v-for="pageSize in pageSizeMenu" :value="pageSize">{{pageSize}}</option>
</select>
    <div class="table-header-wrapper">
      <table class="table-header">
        <thead>
          <th v-for="key in columns"
            @click="sortBy(key)"
            :class="{ active: sortKey == key }"
          >
            {{ key | capitalize }}
            <span class="arrow" :class="sortOrders[key] > 0 ? 'asc' : 'dsc'"></span>
          </th>
        </thead>
      </table>
    </div>
    <div class="table-body-wrapper">
      <table class="table-body">
        <tbody>
          <tr v-for="entry in dataPerPage">
            <td v-for="key in columns"> {{entry[key]}}</td>
          </tr>
        </tbody>
      </table>
    </div>
    <div id="page-navigation">
    <button @click=movePages(-1)>Back</button>
    <p>{{startRow / rowsPerPage + 1}} out of {{Math.ceil(filteredData.length / rowsPerPage)}}</p>
    <button @click=movePages(1)>Next</button>
</div>
  </div>
</div>
</template>

<style>
@import "../assets/styles/gridstyle.css";
</style>

<script>
export default {
  props: {
    data: Array,
    columns: Array,
  },
  data(){
    return {
      startRow: 0,
      rowsPerPage: 10,
      searchQuery: '',
      sortKey: '',
      sortOrders: {},
      pageSizeMenu: [10, 20, 50, 100]
    }
  },
  computed: {
    filteredData: function () {
      let sortKey = this.sortKey;
      let filterKey = this.searchQuery && this.searchQuery.toLowerCase();
      let order = this.sortOrders[sortKey] || 1;
      let data = this.data;

      if (filterKey) {
        data = data.filter(function (row) {
          return Object.keys(row).some(function (key) {
            return String(row[key]).toLowerCase().indexOf(filterKey) > -1;
          })
        })
      }
      if (sortKey) {
        data = data.slice().sort(function (a, b) {
          a = a[sortKey];
          b = b[sortKey];
          return (a === b ? 0 : a > b ? 1 : -1) * order;
        })
      }
    return data;
    },
    dataPerPage: function() {
      return this.filteredData.filter((item, index) => index >= this.startRow && index < (this.startRow + this.rowsPerPage))
  }
  },
  filters: {
    capitalize: function (str) {
      return str.charAt(0).toUpperCase() + str.slice(1);
    }
  },
  methods: {
    sortBy: function (key) {
      this.sortKey = key;
      this.sortOrders[key] = this.sortOrders[key] * -1
    },
    movePages: function(amount) {
      let newStartRow = this.startRow + (amount * this.rowsPerPage);
      if (newStartRow >= 0 && newStartRow < this.filteredData.length) {
        this.startRow = newStartRow;
        }
  }
  },
  created(){
    let sortOrders = {};
    this.columns.forEach(function (key) {
      sortOrders[key] = 1;
    })
    this.sortOrders = sortOrders;
  },
}
</script>
