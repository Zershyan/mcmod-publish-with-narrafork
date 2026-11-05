/**
 * 构建前确认表单的数据。复制为同目录 data.ts 后按工程填。
 * branches 从 `git branch -a` 取，去掉 remotes/ 前缀。
 */
export const DATA = {
	projectName: "模组英文名 · 目录名",
	currentVersion: "0.0.1",
	branches: ["master", "1.20.1", "1.21.1"] as string[],
	defaultBranches: ["master"] as string[],
	/** 需要特别说明时写在这里，会显示成蓝色提示框的列表 */
	hints: [] as string[],
};
