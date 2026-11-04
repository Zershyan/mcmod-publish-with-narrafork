/**
 * 表单数据。复制本文件为同目录的 data.ts，按项目改这里即可，App.tsx 不用动。
 * 字段来源见 skill 的 references/sources.md，凡是工程里读不到的都要先问用户。
 */

export type Version = {
	/** 构建脚本里的 version，可能带 MC 版本与 build 号，按分支实际值填 */
	modVersion: string;
	mcVersions: string[];
	loaders: string[];
	releaseType: string;
	env: string;
	changelog: string;
};

export type Author = { id: string; name: string; role: string };

export type Entry = {
	name: string;
	regname: string;
	type: string;
	damage: string;
	stack: string;
};

export type FormData = {
	modName: string;
	badge: string;
	/** 项目特有许可证，追加到内置列表 */
	extraLicenses?: string[];
	/**
	 * 从 CurseForge Game Versions API 拉到的 MC 版本列表，优先于模板内置候选。
	 * 正常流程先跑 `upload_release.py query`，把返回的版本写进来；拿不到时才省略。
	 */
	mcVersions?: string[];
	iconHint: string;
	coverHint: string;
	/** 没有资料条目时显示的说明 */
	entriesEmptyText: string;
	defaults: Record<string, any>;
	versions: Version[];
	authors: Author[];
	entries: Entry[];
};

export const DATA: FormData = {
	modName: "SnowyCrescentCore",
	badge: "GPL-3.0",
	extraLicenses: ["GPL-3.0-with-additional-terms"],
	iconHint: "默认 logo.png（64×64）",
	coverHint: "logo 仅 64×64，需放大加底色",
	entriesEmptyText: "本项目是纯库模组，语言文件里没有物品、方块与实体，阶段 5 会自动跳过。",
	defaults: {
		cfName: "SnowyCrescentCore",
		cfSummary: "A lib from zershyan.",
		cfDescription: "按工程 README 与源码整理，英文块 + --- + 中文块",
		cfLicense: "GPL-3.0-with-additional-terms",
		cfCategory: "API and Library",
		cfExtraCategories: [],
		cfSourceUrl: "https://github.com/Zershyan/SnowyCrescentCore",

		wName: "（待确认）",
		wEname: "SnowyCrescentCore",
		wIntro: "供其他模组使用的库，提供能力注册、玩家动画与数据生成 API",
		wModid: "sccore",
		wCfId: "阶段 2 建完项目后填入",
		wCore: "LIB",
		wExtra: [],
		wStatus: "活跃",
		wAuthorName: "Zershyan",
		wLinks: "https://github.com/Zershyan/SnowyCrescentCore",
	},
	versions: [
		{
			modVersion: "1.20.1-1.0.1",
			mcVersions: ["1.20.1"],
			loaders: ["Forge"],
			releaseType: "release",
			env: "双端",
			changelog: "",
		},
		{
			modVersion: "2.0.0-1.21.1+build.34",
			mcVersions: ["1.21.1"],
			loaders: ["NeoForge"],
			releaseType: "release",
			env: "双端",
			changelog: "",
		},
	],
	authors: [{ id: "", name: "Zershyan", role: "所有者" }],
	entries: [],
};
