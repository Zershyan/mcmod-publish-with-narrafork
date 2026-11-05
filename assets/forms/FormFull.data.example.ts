/**
 * 表单数据。复制本文件为同目录的 data.ts，只改这里，App.tsx 不用动。
 * 字段含义见 README.md，取值规则见 ../../references/field-sources.md。
 */
export const DATA = {
	/** 模组英文名，显示在标题 */
	modName: "SnowyCrescentCore",
	/** 右上角角标，一般是许可证简称 */
	badge: "GPL-3.0",
	/** 项目特有许可证，追加到内置列表 */
	extraLicenses: ["GPL-3.0-with-additional-terms"],
	/**
	 * 从 CurseForge Game Versions API 拉到的 MC 版本列表，优先于模板内置候选。
	 * 正常流程先跑 `scripts/cf/upload.py query`，把返回的版本写进来；拿不到时才省略。
	 */
	mcVersions: [] as string[],
	iconHint: "默认 logo.png（64×64）",
	coverHint: "logo 仅 64×64，需放大加底色",
	/** 没有资料条目时显示的说明 */
	entriesEmptyText: "本项目是纯库模组，语言文件里没有物品、方块与实体，百科资料条目会自动跳过。",

	/** 所有字段的 placeholder，即调研值；留空的项按这些值执行 */
	defaults: {
		cfName: "SnowyCrescentCore",
		cfSummary: "A lib from zershyan.",
		cfDescription: "按工程 README 与源码整理，英文块 + --- + 中文块",
		cfLicense: "GPL-3.0-with-additional-terms",
		cfCategory: "API and Library",
		cfExtraCategories: [] as string[],
		cfSourceUrl: "https://github.com/Zershyan/SnowyCrescentCore",

		wName: "（待确认）",
		wEname: "SnowyCrescentCore",
		wIntro: "供其他模组使用的库，提供能力注册、玩家动画与数据生成 API",
		wModid: "sccore",
		wCfId: "建完 CF 项目后填入",
		wMrId: "没有就留空",
		wRelations: "代码联动的前置或附属",
		wCore: "LIB",
		wExtra: [] as string[],
		wStatus: "活跃",
		wLicenseType: "源码",
		wLicenseName: "ARR",
		wTags: [] as string[],
		wKeys: [] as string[],
		wAuthorName: "Zershyan",
		wLinks: "https://github.com/Zershyan/SnowyCrescentCore",
	},

	/** 版本条目：modVersion 填 gradle.properties 的 mod_version，只写模组版本，不带 MC 版本和 build 编号 */
	versions: [
		{
			modVersion: "1.0.1",
			mcVersions: ["1.20.1"],
			loaders: ["Forge"],
			javaVersion: "Java 17",
			releaseType: "release",
			env: "双端",
			changelog: "",
		},
		{
			modVersion: "2.0.0",
			mcVersions: ["1.21.1"],
			loaders: ["NeoForge"],
			javaVersion: "Java 21",
			releaseType: "release",
			env: "双端",
			changelog: "",
		},
	],

	authors: [{ id: "", name: "Zershyan", role: "所有者" }],

	/** 资料条目；没有内容物时留空数组。分类取 ENTRY_CATEGORIES 里的值 */
	entries: [] as {
		name: string;
		ename: string;
		regname: string;
		category: string;
		type: string;
		damage: string;
		stack: string;
	}[],

	/**
	 * CurseForge 依赖关系。从 build.gradle 的 `curse.maven:<名>-<项目ID>:<文件ID>` 解析，
	 * jarJar 内嵌与 localRuntime 的不用声明。没有就留空数组。
	 */
	dependencies: [] as { name: string; projectId: string; type: string }[],
};
