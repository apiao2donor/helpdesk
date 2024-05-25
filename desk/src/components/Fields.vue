<template>
  <div class="flex flex-col gap-4">
    <div
      v-for="section in sections"
      :key="section.section"
      class="first:border-t-0 first:pt-0"
      :class="section.hideBorder ? '' : 'border-t pt-4'"
    >
      <div
        class="grid gap-4"
        :class="
          section.columns ? 'grid-cols-' + section.columns : 'grid-cols-3'
        "
      >
        <div v-for="field in section.fields" :key="field.name">
          <div class="mb-2 text-sm text-gray-600">
            {{ __(field.label) }}
            <span v-if="field.mandatory" class="text-red-500">*</span>
          </div>
          <FormControl
            v-if="field.type === 'select'"
            v-model="data[field.name]"
            type="select"
            class="form-control"
            :class="field.prefix ? 'prefix' : ''"
            :options="field.options"
            :placeholder="__(field.placeholder)"
          >
            <template v-if="field.prefix" #prefix>
              <IndicatorIcon :class="field.prefix" />
            </template>
          </FormControl>
          <SearchComplete
            v-else-if="field.type === 'link'"
            class="form-control"
            :value="data[field.name]"
            :doctype="field.doctype"
            :placeholder="field.placeholder"
            :on-create="field.create"
            @change="(v) => (data[field.name] = v)"
          />
          <SearchComplete
            v-else-if="field.type === 'user'"
            class="form-control"
            :value="getUser(data[field.name]).full_name"
            :doctype="field.doctype"
            :placeholder="field.placeholder"
            :hide-me="true"
            @change="(v) => (data[field.name] = v)"
          >
            <template #prefix>
              <UserAvatar class="mr-2" :user="data[field.name]" size="sm" />
            </template>
            <template #item-prefix="{ option }">
              <UserAvatar class="mr-2" :user="option.value" size="sm" />
            </template>
            <template #item-label="{ option }">
              <Tooltip :text="option.value">
                <div class="cursor-pointer">
                  {{ getUser(option.value).full_name }}
                </div>
              </Tooltip>
            </template>
          </SearchComplete>
          <div v-else-if="field.type === 'dropdown'">
            <NestedPopover>
              <template #target="{ open }">
                <Button
                  :label="data[field.name]"
                  class="dropdown-button flex w-full items-center justify-between rounded border border-gray-100 bg-gray-100 px-2 py-1.5 text-base text-gray-800 transition-colors placeholder:text-gray-500 hover:border-gray-200 hover:bg-gray-200 focus:border-gray-500 focus:bg-white focus:shadow-sm focus:outline-none focus:ring-0 focus-visible:ring-2 focus-visible:ring-gray-400"
                >
                  <div class="truncate">{{ data[field.name] }}</div>
                  <template #suffix>
                    <FeatherIcon
                      :name="open ? 'chevron-up' : 'chevron-down'"
                      class="h-4 text-gray-600"
                    />
                  </template>
                </Button>
              </template>
              <template #body>
                <div
                  class="my-2 space-y-1.5 divide-y rounded-lg border border-gray-100 bg-white p-1.5 shadow-xl"
                >
                  <div>
                    <DropdownItem
                      v-for="option in field.options"
                      v-if="field.options?.length"
                      :key="option.name"
                      :option="option"
                    />
                    <div v-else>
                      <div class="p-1.5 px-7 text-base text-gray-500">
                        {{ __("No {0} Available", [field.label]) }}
                      </div>
                    </div>
                  </div>
                  <div class="pt-1.5">
                    <Button
                      variant="ghost"
                      class="w-full !justify-start"
                      :label="__('Create New')"
                      @click="field.create()"
                    >
                      <template #prefix>
                        <FeatherIcon name="plus" class="h-4" />
                      </template>
                    </Button>
                  </div>
                </div>
              </template>
            </NestedPopover>
          </div>
          <FormControl
            v-else
            v-model="data[field.name]"
            type="text"
            :placeholder="__(field.placeholder)"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { Tooltip } from "frappe-ui";
import {
  NestedPopover,
  DropdownItem,
  UserAvatar,
  SearchComplete,
} from "@/components";
import { IndicatorIcon } from "@/components/icons/";
// import { usersStore } from "@/stores/users";

// const { getUser } = usersStore();

const props = defineProps({
  sections: Array,
  data: Object,
});
</script>

<style scoped>
:deep(.form-control.prefix select) {
  padding-left: 2rem;
}
</style>
