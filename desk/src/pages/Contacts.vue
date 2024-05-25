<template>
  <div class="flex flex-col">
    <LayoutHeader>
      <template #left-header>
        <Breadcrumbs :items="breadcrumbs" />
      </template>
      <template #right-header>
        <Button
          label="Create"
          theme="gray"
          variant="solid"
          @click="showModal = true"
        >
          <template #prefix>
            <LucidePlus class="h-4 w-4" />
          </template>
        </Button>
      </template>
    </LayoutHeader>
    <ListView
      :columns="columns.filter((column) => !column.hidden)"
      :rows="contacts?.data?.data || []"
      class="mt-4 px-5"
      :options="{
        getRowRoute: (row) => ({
          name: 'Contact',
          params: { contactId: row.name },
        }),
      }"
    >
      <ListHeader />
      <ListRows>
        <ListRow
          v-for="row in contacts?.data?.data"
          :key="row.name"
          v-slot="{ column, item }"
          :row="row"
        >
          <ListRowItem :item="item">
            <template #prefix>
              <div v-if="column.key === 'name'">
                <Avatar :image="item.image" />
              </div>
            </template>
          </ListRowItem>
        </ListRow>
      </ListRows>
    </ListView>
  </div>
</template>
<script setup lang="ts">
import { ref } from "vue";
import {
  Breadcrumbs,
  ListView,
  Avatar,
  createResource,
  ListRows,
  ListRow,
  ListRowItem,
  ListHeader,
} from "frappe-ui";
import { LayoutHeader } from "@/components";

const showModal = ref(false);
const breadcrumbs = [{ label: "Contacts", route: { name: "ContactList" } }];
const columns = [
  {
    label: "Name",
    key: "name",
    width: "15rem",
  },
  {
    label: "Email",
    key: "email_id",
    width: "15rem",
  },
  {
    label: "Phone",
    key: "phone",
    width: "15rem",
  },
  {
    label: "Image",
    key: "image",
    width: "15rem",
    hidden: 1,
  },
];

const contacts = createResource({
  url: "helpdesk.api.doc.get_list_data",
  fields: ["name", "email_id", "image", "phone"],
  params: {
    doctype: "Contact",
    columns: columns,
  },
  auto: true,
});
</script>
