/**
 * 发布配置表单模板。
 * 复制本文件与同目录的 data.ts 到 .narrafork/gen_ui/<名称>/ 后 show 该目录。
 * 项目差异全部写在 data.ts，本文件不需要改动。
 */
import { useState } from "react";
import {
	ActionIcon,
	Autocomplete,
	Badge,
	Box,
	Button,
	Card,
	Checkbox,
	FileButton,
	Grid,
	Group,
	Input,
	Modal,
	MultiSelect,
	Select,
	Stack,
	Switch,
	Table,
	Tabs,
	TagsInput,
	Text,
	Textarea,
	TextInput,
	Title,
	UnstyledButton,
} from "@mantine/core";
import { DATA } from "./data";

type Version = {
	modVersion: string;
	mcVersions: string[];
	loaders: string[];
	/** CurseForge 版本标签中的 Java 版本，如 "Java 21" */
	javaVersion: string;
	releaseType: string;
	env: string;
	changelog: string;
};
type Author = { id: string; name: string; role: string };
type Dependency = { name: string; projectId: string; type: string };
type Entry = {
	name: string;
	/** 百科次要名称，取自 en_us.json */
	ename: string;
	regname: string;
	/** 百科资料分类，取值见 ENTRY_CATEGORIES */
	category: string;
	type: string;
	damage: string;
	stack: string;
};
type FormData = {
	modName: string;
	badge: string;
	extraLicenses?: string[];
	mcVersions?: string[];
	iconHint: string;
	coverHint: string;
	entriesEmptyText: string;
	defaults: Record<string, any>;
	versions: Version[];
	authors: Author[];
	entries: Entry[];
	dependencies?: Dependency[];
};

const D = DATA as FormData;

/** CurseForge 分类及中文对照 */
const CF_CATEGORIES: { value: string; zh: string }[] = [
	{ value: "Adventure and RPG", zh: "冒险与角色扮演" },
	{ value: "API and Library", zh: "API 与前置" },
	{ value: "Armor, Tools, and Weapons", zh: "装备与武器" },
	{ value: "Cosmetic", zh: "外观装饰" },
	{ value: "Decoration", zh: "装饰" },
	{ value: "Map and Information", zh: "地图与信息" },
	{ value: "Mobs", zh: "生物" },
	{ value: "Miscellaneous", zh: "杂项" },
	{ value: "Server Utility", zh: "服务器实用" },
	{ value: "Technology", zh: "科技" },
	{ value: "World Gen", zh: "世界生成" },
	{ value: "Addons", zh: "附属" },
];
const CF_VALUES = CF_CATEGORIES.map((item) => item.value);
const CF_ZH: Record<string, string> = Object.fromEntries(
	CF_CATEGORIES.map((item) => [item.value, item.zh]),
);

const LOADERS = ["NeoForge", "Forge", "Fabric"];
const RELEASE_TYPES = ["release", "beta", "alpha"];
const ENVS = ["双端", "仅客户端", "仅服务端"];
const CORE_ELEMENTS = ["实用", "科技", "魔法", "冒险", "农业", "装饰", "LIB", "魔改", "辅助"];
const LICENSE_TYPES = ["源码", "资产", "构件", "其他"];
const LICENSE_NAMES = [
	"ARR", "MIT", "AGPL-3.0", "GPL-3.0", "GPL-2.0", "LGPL-3.0",
	"Apache-2.0", "MPL-2.0", "BSD-3-Clause", "CC-BY-4.0", "CC-BY-SA-4.0",
];
const ROLES = ["所有者", "程序", "美术", "音效", "策划", "文案", "建筑", "贡献者", "吉祥物", "自定义"];
const WIKI_STATUS = ["不确定", "活跃", "半弃坑", "停更"];
const WIKI_SOURCE = ["不显示", "开源", "闭源"];
const DEP_TYPES = [
	{ value: "required", label: "必需前置" },
	{ value: "optional", label: "可选前置" },
	{ value: "incompatible", label: "不兼容" },
];
const JAVA_VERSIONS = ["Java 8", "Java 11", "Java 17", "Java 21", "Java 25"];
/** 百科资料分类，与添加页 data-multi-value 顺序一致 */
const ENTRY_CATEGORIES = [
	"物品/方块",
	"群系/群落",
	"世界/维度",
	"生物/实体",
	"附魔/魔咒",
	"BUFF/DEBUFF",
	"多方块结构",
	"自然生成",
	"绑定热键",
	"游戏设定",
];
const BASE_LICENSES = ["GNU AGPL 3.0", "GPL 3.0", "LGPL 3.0", "MIT", "Apache 2.0", "All Rights Reserved"];

/**
 * 兜底候选：没跑 Game Versions API 时用。
 * 正常流程先 query 出真实版本列表写进 data.ts 的 mcVersions，这里只是应急。
 */
const FALLBACK_MC_VERSIONS = [
	"26.3", "26.2", "26.1.2", "26.1.1", "26.1",
	"1.21.11", "1.21.10", "1.21.9", "1.21.8", "1.21.7", "1.21.6", "1.21.5",
	"1.21.4", "1.21.3", "1.21.2", "1.21.1", "1.21",
	"1.20.6", "1.20.5", "1.20.4", "1.20.3", "1.20.2", "1.20.1", "1.20",
	"1.19.4", "1.19.3", "1.19.2", "1.19.1", "1.19",
	"1.18.2", "1.18.1", "1.18",
	"1.17.1", "1.17",
	"1.16.5", "1.16.4", "1.16.3", "1.16.2", "1.16.1", "1.16",
	"1.15.2", "1.15.1", "1.15",
	"1.14.4", "1.14.3", "1.14.2", "1.14.1", "1.14",
	"1.13.2", "1.13.1", "1.13",
	"1.12.2", "1.12.1", "1.12",
	"1.11.2", "1.11.1", "1.11",
	"1.10.2", "1.10.1", "1.10",
	"1.9.4", "1.9.3", "1.9.2", "1.9.1", "1.9",
	"1.8.9", "1.8.8", "1.8.7", "1.8.6", "1.8.5", "1.8.4", "1.8.3", "1.8.2", "1.8.1", "1.8",
	"1.7.10", "1.7.2",
	"1.6.4", "1.6.2", "1.6.1",
	"1.5.2", "1.5.1",
	"1.4.7",
	"1.3.2", "1.3.1",
	"1.2.5",
	"1.1",
	"1.0",
];

/** 优先用 API 拉到的完整列表，没提供时才退回兜底候选 */
const MC_VERSIONS = D.mcVersions ?? FALLBACK_MC_VERSIONS;

const LICENSES = Array.from(new Set([...BASE_LICENSES, ...(D.extraLicenses ?? [])]));
/** 除 All Rights Reserved 外都视为开源许可 */
const isOpenSource = (license: string) => license !== "All Rights Reserved";

const envToSides = (env: string): [string, string] => {
	if (env === "仅客户端") return ["需装", "无需"];
	if (env === "仅服务端") return ["无需", "需装"];
	return ["需装", "需装"];
};

const emptyVersion = (): Version => ({
	modVersion: "",
	mcVersions: [],
	loaders: [],
	javaVersion: "Java 21",
	releaseType: "release",
	env: ENVS[0],
	changelog: "",
});

export default function App() {
	const [wiki, setWiki] = useState(false);
	const [tab, setTab] = useState<string | null>("cf");
	const [v, setV] = useState<Record<string, any>>({});
	const [distTouched, setDistTouched] = useState(false);
	const [versionsOpen, setVersionsOpen] = useState(true);

	const [versions, setVersions] = useState<Version[]>(D.versions);
	const [expanded, setExpanded] = useState<boolean[]>(D.versions.map(() => true));
	const [authors, setAuthors] = useState<Author[]>(D.authors);
	const [deps, setDeps] = useState<Dependency[]>(D.dependencies ?? []);
	const [cfIcon, setCfIcon] = useState<File | null>(null);
	const [wCover, setWCover] = useState<File | null>(null);

	const [entries, setEntries] = useState<Entry[]>(D.entries);
	const [editing, setEditing] = useState<number | null>(null);
	const [draft, setDraft] = useState<Entry | null>(null);

	const [newVersionOpen, setNewVersionOpen] = useState(false);
	const [newVersion, setNewVersion] = useState<Version>(emptyVersion());

	const [wikiTargets, setWikiTargets] = useState<string[] | null>(null);
	const [targetOpen, setTargetOpen] = useState(false);
	const [targetDraft, setTargetDraft] = useState<{ loaders: string[]; mcVersions: string[] }>({
		loaders: [],
		mcVersions: [],
	});

	const text = (k: string) => ({
		value: (v[k] as string) ?? "",
		onChange: (e: any) => setV((s) => ({ ...s, [k]: e.currentTarget.value })),
	});
	const pick = (k: string) => ({
		value: (v[k] as string) ?? null,
		onChange: (val: any) => setV((s) => ({ ...s, [k]: val })),
	});
	const multi = (k: string) => ({
		value: (v[k] as string[]) ?? [],
		onChange: (val: any) => setV((s) => ({ ...s, [k]: val })),
	});

	const license = (v.cfLicense as string) ?? D.defaults.cfLicense;
	const distribute =
		v.cfDistribute === undefined ? isOpenSource(license) : Boolean(v.cfDistribute);
	const comments = v.cfComments === undefined ? true : Boolean(v.cfComments);

	const allMcVersions = Array.from(new Set(versions.flatMap((item) => item.mcVersions)));
	const allLoaders = Array.from(new Set(versions.flatMap((item) => item.loaders)));
	const firstEnv = versions[0]?.env ?? ENVS[0];

	const cfTargets = Array.from(
		new Set(
			versions.flatMap((item) =>
				item.loaders.flatMap((loader) => item.mcVersions.map((mc) => `${loader} ${mc}`)),
			),
		),
	);
	const targets = wikiTargets ?? cfTargets;

	const confirmTargets = () => {
		const combos = targetDraft.loaders.flatMap((loader) =>
			targetDraft.mcVersions.map((mc) => `${loader} ${mc}`),
		);
		setWikiTargets(Array.from(new Set([...targets, ...combos])));
		setTargetDraft({ loaders: [], mcVersions: [] });
		setTargetOpen(false);
	};
	const removeTarget = (value: string) =>
		setWikiTargets(targets.filter((item) => item !== value));

	const derivedSource = isOpenSource(license) ? "开源" : "闭源";
	const [derivedClient, derivedServer] = envToSides(firstEnv);

	const onLicense = (val: string | null) => {
		const next = val ?? "";
		setV((s) => ({
			...s,
			cfLicense: next,
			cfDistribute: distTouched ? s.cfDistribute : isOpenSource(next),
		}));
	};

	const setVersion = (index: number, patch: Partial<Version>) =>
		setVersions((list) => list.map((item, i) => (i === index ? { ...item, ...patch } : item)));
	const removeVersion = (index: number) => {
		setVersions((list) => list.filter((_, i) => i !== index));
		setExpanded((list) => list.filter((_, i) => i !== index));
	};
	const toggleVersion = (index: number) =>
		setExpanded((list) => list.map((open, i) => (i === index ? !open : open)));

	const confirmNewVersion = () => {
		setVersions((list) => [...list, newVersion]);
		setExpanded((list) => [...list, true]);
		setNewVersion(emptyVersion());
		setNewVersionOpen(false);
	};

	const setAuthor = (index: number, patch: Partial<Author>) =>
		setAuthors((list) => list.map((item, i) => (i === index ? { ...item, ...patch } : item)));
	const addAuthor = () => setAuthors((list) => [...list, { id: "", name: "", role: "开发者" }]);
	const removeAuthor = (index: number) => setAuthors((list) => list.filter((_, i) => i !== index));

	const setDep = (index: number, patch: Partial<Dependency>) =>
		setDeps((list) => list.map((item, i) => (i === index ? { ...item, ...patch } : item)));
	const addDep = () =>
		setDeps((list) => [...list, { name: "", projectId: "", type: "required" }]);
	const removeDep = (index: number) => setDeps((list) => list.filter((_, i) => i !== index));

	const editEntry = (index: number) => {
		setEditing(index);
		setDraft({ ...entries[index] });
	};
	const confirmEntry = () => {
		if (editing === null || !draft) return;
		setEntries((list) => list.map((item, i) => (i === editing ? draft : item)));
		setEditing(null);
		setDraft(null);
	};
	const addEntry = () => {
		const created: Entry = {
			name: "",
			ename: "",
			regname: "",
			category: "物品/方块",
			type: "道具",
			damage: "-",
			stack: "1",
		};
		setEntries((list) => [...list, created]);
		setEditing(entries.length);
		setDraft({ ...created });
	};
	const removeEntry = (index: number) => setEntries((list) => list.filter((_, i) => i !== index));

	const submit = () => {
		const out: Record<string, any> = { 发布到百科: wiki };
		for (const [key, fallback] of Object.entries(D.defaults)) {
			const current = v[key];
			const empty =
				current === undefined ||
				current === "" ||
				(Array.isArray(current) && current.length === 0);
			out[key] = empty ? fallback : current;
		}
		out.cfDistribute = distribute;
		out.cfComments = comments;
		out.cfIcon = cfIcon?.name ?? "src/main/resources/logo.png";
		out.wCover = wCover?.name ?? "src/main/resources/logo.png";
		out.wSource = (v.wSource as string) ?? derivedSource;
		out.wikiTargets = targets;
		out.wClient = (v.wClient as string) ?? derivedClient;
		out.wServer = (v.wServer as string) ?? derivedServer;
		out.versions = versions;
		out.authors = authors;
		out.entries = entries;
		out.dependencies = deps;
		(globalThis as any).genUI?.submit(
			out,
			wiki ? "按此配置发布到 CurseForge 与 MC百科" : "按此配置发布到 CurseForge",
		);
	};

	const cfOption = ({ option }: any) => (
		<Group justify="space-between" w="100%" wrap="nowrap">
			<Text size="sm">{option.value}</Text>
			<Text size="xs" c="dimmed">
				{CF_ZH[option.value] ?? ""}
			</Text>
		</Group>
	);

	const picker = (label: string, value: File | null, onChange: any, hint: string) => (
		<Input.Wrapper label={label}>
			<Group gap="xs" h={36} align="center" wrap="nowrap">
				<FileButton onChange={onChange} accept="image/png,image/jpeg">
					{(props) => (
						<Button variant="default" size="xs" {...props}>
							选择文件
						</Button>
					)}
				</FileButton>
				<Text size="xs" c="dimmed" truncate>
					{value ? value.name : hint}
				</Text>
			</Group>
		</Input.Wrapper>
	);

	return (
		<Box p="lg">
			<Group justify="space-between" align="flex-start" mb="md">
				<Stack gap={2}>
					<Title order={3}>发布配置</Title>
					<Text size="sm" c="dimmed">
						{D.modName} · {allLoaders.join(" / ")} · {allMcVersions.join(" / ")}
					</Text>
				</Stack>
				<Badge variant="light" size="lg">
					{D.badge}
				</Badge>
			</Group>

			<Card withBorder shadow="sm" radius="md" p="md" mb="md">
				<Checkbox
					checked={wiki}
					onChange={(e) => {
						const on = e.currentTarget.checked;
						setWiki(on);
						if (!on) setTab("cf");
					}}
					label="同时发布到 MC百科"
					description="CurseForge 必发；百科条目依赖 CF Project ID，可以不发。勾选后出现百科配置。"
				/>
			</Card>

			<Tabs value={tab} onChange={setTab} variant="pills" radius="md">
				<Tabs.List mb="md">
					<Tabs.Tab value="cf">CurseForge</Tabs.Tab>
					{wiki && <Tabs.Tab value="wiki">MC百科</Tabs.Tab>}
				</Tabs.List>

				<Tabs.Panel value="cf">
					<Stack gap="md">
						<Card withBorder shadow="sm" radius="md" p="md">
							<Group justify="space-between" mb="sm">
								<Text fw={600}>项目信息</Text>
								<Badge size="xs" variant="light" color="gray">
									灰色提示为调研自动填入
								</Badge>
							</Group>
							<Grid gutter="sm">
								<Grid.Col span={4}>
									<TextInput
										label="项目名"
										placeholder={D.defaults.cfName}
										{...text("cfName")}
									/>
								</Grid.Col>
								<Grid.Col span={4}>
									<Select
										label="许可证"
										data={LICENSES}
										value={license}
										onChange={onLicense}
										searchable
									/>
								</Grid.Col>
								<Grid.Col span={4}>
									<Input.Wrapper label="允许第三方分发">
										<Group h={36} align="center" gap="xs" wrap="nowrap">
											<Switch
												checked={distribute}
												onChange={(e) => {
													setDistTouched(true);
													setV((s) => ({ ...s, cfDistribute: e.currentTarget.checked }));
												}}
											/>
											<Text size="xs" c="dimmed">
												{isOpenSource(license) ? "开源许可，默认允许" : "闭源许可，默认关闭"}
											</Text>
										</Group>
									</Input.Wrapper>
								</Grid.Col>
								<Grid.Col span={12}>
									<TextInput
										label="简介"
										description="1～256 字符"
										placeholder={D.defaults.cfSummary}
										{...text("cfSummary")}
									/>
								</Grid.Col>
								<Grid.Col span={12}>
									<Textarea
										label="详细描述"
										description="留空则按工程 README 与源码整理"
										placeholder={D.defaults.cfDescription}
										minRows={2}
										autosize
										{...text("cfDescription")}
									/>
								</Grid.Col>
								<Grid.Col span={7}>
									<Autocomplete
										label="主分类"
										withAsterisk
										data={CF_VALUES}
										renderOption={cfOption}
										placeholder={D.defaults.cfCategory}
										{...pick("cfCategory")}
									/>
								</Grid.Col>
								<Grid.Col span={5}>
									<MultiSelect
										label="附加分类"
										data={CF_VALUES}
										renderOption={cfOption}
										placeholder="可选"
										clearable
										{...multi("cfExtraCategories")}
									/>
								</Grid.Col>
								<Grid.Col span={7}>
									{picker(
										"项目图标（超过 400px 自动缩放）",
										cfIcon,
										setCfIcon,
										D.iconHint,
									)}
								</Grid.Col>
								<Grid.Col span={5}>
									<Input.Wrapper label="允许评论">
										<Group h={36} align="center">
											<Switch
												checked={comments}
												onChange={(e) =>
													setV((s) => ({ ...s, cfComments: e.currentTarget.checked }))
												}
											/>
										</Group>
									</Input.Wrapper>
								</Grid.Col>
								<Grid.Col span={12}>
									<TextInput
										label="源码链接"
										description="创建向导里没有这一项时，建完项目在项目设置 → Links → Source 补"
										placeholder={D.defaults.cfSourceUrl}
										{...text("cfSourceUrl")}
									/>
								</Grid.Col>
							</Grid>
						</Card>

						<Card withBorder shadow="sm" radius="md" p="md">
							<Group justify="space-between" mb="sm">
								<Group gap="xs">
									<Text fw={600}>依赖关系</Text>
									<Badge size="xs" variant="light" color="gray">
										从 build.gradle 解析，内嵌与仅运行时的不声明
									</Badge>
								</Group>
								<Button size="compact-sm" variant="light" onClick={addDep}>
									+ 添加依赖
								</Button>
							</Group>
							{deps.length === 0 ? (
								<Text size="sm" c="dimmed">
									没有需要声明的前置模组
								</Text>
							) : (
								<Stack gap="sm">
									{deps.map((dep, index) => (
										<Group key={index} align="flex-end" gap="sm" wrap="nowrap">
											<TextInput
												label={index === 0 ? "模组名" : undefined}
												placeholder="Curios"
												value={dep.name}
												onChange={(e) => setDep(index, { name: e.currentTarget.value })}
												style={{ flex: 1 }}
											/>
											<TextInput
												label={index === 0 ? "CF 项目 ID" : undefined}
												placeholder="309927"
												value={dep.projectId}
												onChange={(e) => setDep(index, { projectId: e.currentTarget.value })}
												style={{ flex: 1 }}
											/>
											<Select
												label={index === 0 ? "关系" : undefined}
												data={DEP_TYPES}
												value={dep.type}
												onChange={(val) => setDep(index, { type: val ?? "required" })}
												style={{ flex: 1 }}
											/>
											<ActionIcon
												size="lg"
												variant="subtle"
												color="red"
												onClick={() => removeDep(index)}
												aria-label="删除依赖"
											>
												×
											</ActionIcon>
										</Group>
									))}
								</Stack>
							)}
						</Card>

						<Card withBorder shadow="sm" radius="md" p="md">
							<Group justify="space-between" mb={versionsOpen ? "sm" : 0}>
								<UnstyledButton onClick={() => setVersionsOpen((open) => !open)}>
									<Group gap="xs">
										<Text fw={600}>版本与上传设置</Text>
										<Badge size="sm" variant="light">
											{versions.length} 个版本
										</Badge>
									</Group>
								</UnstyledButton>
								<Button size="compact-sm" variant="light" onClick={() => setNewVersionOpen(true)}>
									+ 添加版本
								</Button>
							</Group>

							{versionsOpen && (
								<Stack gap="sm">
									{versions.map((item, index) => (
										<Card key={index} withBorder radius="sm" p="sm">
											<Group justify="space-between" mb={expanded[index] ? "xs" : 0}>
												<UnstyledButton onClick={() => toggleVersion(index)}>
													<Group gap="xs">
														<Text size="sm" fw={500}>
															版本 {index + 1}
														</Text>
														<Text size="xs" c="dimmed">
															{item.modVersion} · {item.loaders.join("+")} ·{" "}
															{item.mcVersions.join(" / ")}
														</Text>
													</Group>
												</UnstyledButton>
												{versions.length > 1 && (
													<ActionIcon
														size="sm"
														variant="subtle"
														color="red"
														onClick={() => removeVersion(index)}
														aria-label="删除版本"
													>
														×
													</ActionIcon>
												)}
											</Group>
											{expanded[index] && (
												<Grid gutter="sm">
													<Grid.Col span={4}>
														<TextInput
															label="mod 版本"
															placeholder="1.2.0+1.21.1"
															value={item.modVersion}
															onChange={(e) =>
																setVersion(index, { modVersion: e.currentTarget.value })
															}
														/>
													</Grid.Col>
													<Grid.Col span={4}>
														<TagsInput
															label="MC 版本"
															data={MC_VERSIONS}
															value={item.mcVersions}
															onChange={(val) => setVersion(index, { mcVersions: val })}
															clearable
														/>
													</Grid.Col>
													<Grid.Col span={4}>
														<MultiSelect
															label="加载器"
															data={LOADERS}
															value={item.loaders}
															onChange={(val) => setVersion(index, { loaders: val })}
															clearable
														/>
													</Grid.Col>
													<Grid.Col span={4}>
														<Select
															label="Java 版本"
															data={JAVA_VERSIONS}
															value={item.javaVersion}
															onChange={(val) =>
																setVersion(index, { javaVersion: val ?? "Java 21" })
															}
														/>
													</Grid.Col>
													<Grid.Col span={4}>
														<Select
															label="发布类型"
															data={RELEASE_TYPES}
															value={item.releaseType}
															onChange={(val) =>
																setVersion(index, { releaseType: val ?? "release" })
															}
														/>
													</Grid.Col>
													<Grid.Col span={4}>
														<Select
															label="运行环境"
															data={ENVS}
															value={item.env}
															onChange={(val) => setVersion(index, { env: val ?? ENVS[0] })}
														/>
													</Grid.Col>
													<Grid.Col span={12}>
														<Textarea
															label="更新说明"
															description="留空则按 git 提交记录整理，英文块 + --- + 中文块"
															placeholder="可选"
															minRows={2}
															autosize
															value={item.changelog}
															onChange={(e) =>
																setVersion(index, { changelog: e.currentTarget.value })
															}
														/>
													</Grid.Col>
												</Grid>
											)}
										</Card>
									))}
								</Stack>
							)}
						</Card>
					</Stack>
				</Tabs.Panel>

				{wiki && (
					<Tabs.Panel value="wiki">
						<Stack gap="md">
							<Card withBorder shadow="sm" radius="md" p="md">
								<Group justify="space-between" mb="sm">
									<Text fw={600}>条目信息</Text>
									<Badge size="xs" variant="light" color="gray">
										灰色提示为调研自动填入
									</Badge>
								</Group>
								<Grid gutter="sm">
									<Grid.Col span={6}>
										<TextInput
											label="主要名称（中文）"
											withAsterisk
											placeholder={D.defaults.wName}
											{...text("wName")}
										/>
									</Grid.Col>
									<Grid.Col span={6}>
										<TextInput
											label="次要名称（英文）"
											placeholder={D.defaults.wEname}
											{...text("wEname")}
										/>
									</Grid.Col>
									<Grid.Col span={12}>
										<TextInput
											label="一句话简介"
											placeholder={D.defaults.wIntro}
											{...text("wIntro")}
										/>
									</Grid.Col>
									<Grid.Col span={4}>
										<TextInput
											label="MODID"
											withAsterisk
											placeholder={D.defaults.wModid}
											{...text("wModid")}
										/>
									</Grid.Col>
									<Grid.Col span={4}>
										<TextInput
											label="CurseForge Project ID"
											placeholder={D.defaults.wCfId}
											{...text("wCfId")}
										/>
									</Grid.Col>
									<Grid.Col span={4}>
										<TextInput
											label="Modrinth Project ID（可空）"
											placeholder={D.defaults.wMrId}
											{...text("wMrId")}
										/>
									</Grid.Col>
									<Grid.Col span={4}>
										<Select
											label="核心元素（单选）"
											withAsterisk
											data={CORE_ELEMENTS}
											placeholder={D.defaults.wCore}
											{...pick("wCore")}
										/>
									</Grid.Col>
									<Grid.Col span={8}>
										<MultiSelect
											label="杂项元素"
											data={["道具", "国创", "物流", "能源", "信息", "魔改", "实用", "辅助"]}
											placeholder="可选"
											clearable
											{...multi("wExtra")}
										/>
									</Grid.Col>
									<Grid.Col span={4}>
										<Select
											label="官方状态"
											data={WIKI_STATUS}
											placeholder={D.defaults.wStatus}
											{...pick("wStatus")}
										/>
									</Grid.Col>
									<Grid.Col span={4}>
										<Select
											label="开源状态"
											data={WIKI_SOURCE}
											placeholder={derivedSource}
											{...pick("wSource")}
										/>
									</Grid.Col>
									<Grid.Col span={4}>
										{picker("封面（16:10）", wCover, setWCover, D.coverHint)}
									</Grid.Col>
								</Grid>
							</Card>

							<Card withBorder shadow="sm" radius="md" p="md">
								<Group justify="space-between" mb="sm">
									<Text fw={600}>作者</Text>
									<Button size="compact-sm" variant="light" onClick={addAuthor}>
										+ 添加作者
									</Button>
								</Group>
								<Stack gap="sm">
									{authors.map((item, index) => (
										<Group key={index} align="flex-end" gap="sm" wrap="nowrap">
											<TextInput
												label={index === 0 ? "作者 ID" : undefined}
												withAsterisk={index === 0}
												placeholder="作者页 /author/数字.html 里的 ID"
												value={item.id}
												onChange={(e) => setAuthor(index, { id: e.currentTarget.value })}
												style={{ flex: 1 }}
											/>
											<TextInput
												label={index === 0 ? "作者名" : undefined}
												placeholder={
													index === 0 ? D.defaults.wAuthorName ?? "作者名" : "作者名"
												}
												value={item.name}
												onChange={(e) => setAuthor(index, { name: e.currentTarget.value })}
												style={{ flex: 1 }}
											/>
											<Autocomplete
												label={index === 0 ? "职位" : undefined}
												data={ROLES}
												filter={({ options }) => options}
												placeholder="可选择或自定义"
												value={item.role}
												onChange={(val) => setAuthor(index, { role: val })}
												style={{ flex: 1 }}
											/>
											<ActionIcon
												size="lg"
												variant="subtle"
												color="red"
												disabled={authors.length === 1}
												onClick={() => removeAuthor(index)}
												aria-label="删除作者"
											>
												×
											</ActionIcon>
										</Group>
									))}
								</Stack>
							</Card>

							<Card withBorder shadow="sm" radius="md" p="md">
								<Text fw={600} mb="sm">
									许可协议
								</Text>
								<Grid gutter="sm">
									<Grid.Col span={4}>
										<Select
											label="协议类型"
											data={LICENSE_TYPES}
											placeholder={D.defaults.wLicenseType}
											{...pick("wLicenseType")}
										/>
									</Grid.Col>
									<Grid.Col span={8}>
										<Autocomplete
											label="协议名称"
											data={LICENSE_NAMES}
											placeholder={D.defaults.wLicenseName}
											{...pick("wLicenseName")}
										/>
									</Grid.Col>
								</Grid>
								<Text size="xs" c="dimmed" mt="xs">
									留空表示不填；ARR 表示保留所有权利。版本范围默认「通用」，提交时为空。
								</Text>
							</Card>

							<Card withBorder shadow="sm" radius="md" p="md">
								<Text fw={600} mb="sm">
									运行与链接
								</Text>
								<Grid gutter="sm">
									<Grid.Col span={8}>
										<Input.Wrapper label="运作方式与版本">
											<Box
												style={{
													minHeight: 36,
													border: "1px solid var(--mantine-color-default-border)",
													borderRadius: "var(--mantine-radius-sm)",
													padding: "4px 8px",
													display: "flex",
													flexWrap: "wrap",
													gap: 6,
													alignItems: "center",
												}}
											>
												{targets.map((item) => (
													<Badge
														key={item}
														size="md"
														variant="light"
														tt="none"
														rightSection={
															<Text
																component="span"
																onClick={() => removeTarget(item)}
																style={{ cursor: "pointer" }}
															>
																×
															</Text>
														}
													>
														{item}
													</Badge>
												))}
												<ActionIcon
													size="sm"
													variant="subtle"
													onClick={() => setTargetOpen(true)}
													aria-label="添加运作方式与版本"
												>
													+
												</ActionIcon>
												{wikiTargets !== null && (
													<Button
														size="compact-xs"
														variant="subtle"
														onClick={() => setWikiTargets(null)}
													>
														恢复跟随 CurseForge
													</Button>
												)}
											</Box>
										</Input.Wrapper>
									</Grid.Col>
									<Grid.Col span={2}>
										<Select
											label="客户端"
											data={["需装", "可选", "无需"]}
											placeholder={derivedClient}
											{...pick("wClient")}
										/>
									</Grid.Col>
									<Grid.Col span={2}>
										<Select
											label="服务端"
											data={["需装", "可选", "无需"]}
											placeholder={derivedServer}
											{...pick("wServer")}
										/>
									</Grid.Col>
									<Grid.Col span={12}>
										<Textarea
											label="模组关系"
											description="代码联动的前置或附属，如「JEI（联动）、Jade（联动）」"
											placeholder={D.defaults.wRelations}
											minRows={2}
											autosize
											{...text("wRelations")}
										/>
									</Grid.Col>
									<Grid.Col span={12}>
										<Textarea
											label="相关链接"
											description="CF 项目页会自动补，其余一行一个"
											placeholder={D.defaults.wLinks}
											minRows={2}
											autosize
											{...text("wLinks")}
										/>
									</Grid.Col>
								</Grid>
								<Text size="xs" c="dimmed" mt="xs">
									默认跟随 CurseForge 的所有「加载器 × MC 版本」组合；手动增删后停止同步，可点「恢复跟随」还原。
								</Text>
							</Card>

							<Card withBorder shadow="sm" radius="md" p="md">
								<Group justify="space-between" mb="sm">
									<Group gap="xs">
										<Text fw={600}>资料条目</Text>
										<Badge size="xs" variant="light" color="gray">
											{entries.length} 条示意 · 实际由工程注册项生成
										</Badge>
									</Group>
									<Button size="compact-sm" variant="light" onClick={addEntry}>
										+ 添加条目
									</Button>
								</Group>
								{entries.length === 0 ? (
									<Text size="sm" c="dimmed">
										{D.entriesEmptyText}
									</Text>
								) : (
									<Table striped highlightOnHover withTableBorder>
										<Table.Thead>
											<Table.Tr>
												<Table.Th w={56}>图标</Table.Th>
												<Table.Th>名称</Table.Th>
												<Table.Th w={110}>分类</Table.Th>
												<Table.Th>注册名</Table.Th>
												<Table.Th w={100}>资料类型</Table.Th>
												<Table.Th w={70}>耐久</Table.Th>
												<Table.Th w={60}>堆叠</Table.Th>
												<Table.Th w={80}>操作</Table.Th>
											</Table.Tr>
										</Table.Thead>
										<Table.Tbody>
											{entries.map((entry, index) => (
												<Table.Tr key={index}>
													<Table.Td>
														<Box w={32} h={32} bg="var(--mantine-color-default-border)" />
													</Table.Td>
													<Table.Td>
														<Text size="sm">{entry.name || "未命名"}</Text>
														<Text size="xs" c="dimmed">
															{entry.ename}
														</Text>
													</Table.Td>
													<Table.Td>
														<Text size="sm">{entry.category}</Text>
													</Table.Td>
													<Table.Td>
														<Text size="xs" c="dimmed" ff="monospace">
															{entry.regname || "-"}
														</Text>
													</Table.Td>
													<Table.Td>
														<Text size="sm">{entry.type}</Text>
													</Table.Td>
													<Table.Td>
														<Text size="sm">{entry.damage}</Text>
													</Table.Td>
													<Table.Td>
														<Text size="sm">{entry.stack}</Text>
													</Table.Td>
													<Table.Td>
														<Group gap={4} wrap="nowrap">
															<ActionIcon
																size="sm"
																variant="subtle"
																onClick={() => editEntry(index)}
															>
																✎
															</ActionIcon>
															<ActionIcon
																size="sm"
																variant="subtle"
																color="red"
																onClick={() => removeEntry(index)}
															>
																×
															</ActionIcon>
														</Group>
													</Table.Td>
												</Table.Tr>
											))}
										</Table.Tbody>
									</Table>
								)}
								<Text size="xs" c="dimmed" mt="xs">
									名称与注册名取自语言文件和注册表，耐久与堆叠来自运行时导出。
								</Text>
							</Card>
						</Stack>
					</Tabs.Panel>
				)}
			</Tabs>

			<Group mt="lg" justify="space-between" align="center">
				<Text size="xs" c="dimmed">
					留空的项按灰色提示值执行
				</Text>
				<Button onClick={submit} radius="md">
					提交配置
				</Button>
			</Group>

			<Modal opened={newVersionOpen} onClose={() => setNewVersionOpen(false)} title="新建版本">
				<Stack gap="sm">
					<TextInput
						label="mod 版本"
						placeholder="1.2.0+1.21.1"
						value={newVersion.modVersion}
						onChange={(e) => setNewVersion({ ...newVersion, modVersion: e.currentTarget.value })}
					/>
					<TagsInput
						label="MC 版本"
						data={MC_VERSIONS}
						value={newVersion.mcVersions}
						onChange={(val) => setNewVersion({ ...newVersion, mcVersions: val })}
						clearable
					/>
					<MultiSelect
						label="加载器"
						data={LOADERS}
						value={newVersion.loaders}
						onChange={(val) => setNewVersion({ ...newVersion, loaders: val })}
						clearable
					/>
					<Select
						label="Java 版本"
						data={JAVA_VERSIONS}
						value={newVersion.javaVersion}
						onChange={(val) => setNewVersion({ ...newVersion, javaVersion: val ?? "Java 21" })}
					/>
					<Select
						label="发布类型"
						data={RELEASE_TYPES}
						value={newVersion.releaseType}
						onChange={(val) => setNewVersion({ ...newVersion, releaseType: val ?? "release" })}
					/>
					<Group justify="flex-end" mt="xs">
						<Button variant="default" onClick={() => setNewVersionOpen(false)}>
							取消
						</Button>
						<Button onClick={confirmNewVersion}>确定</Button>
					</Group>
				</Stack>
			</Modal>

			<Modal opened={targetOpen} onClose={() => setTargetOpen(false)} title="添加运作方式与版本">
				<Stack gap="sm">
					<MultiSelect
						label="加载器"
						data={LOADERS}
						value={targetDraft.loaders}
						onChange={(val) => setTargetDraft({ ...targetDraft, loaders: val })}
						clearable
					/>
					<TagsInput
						label="MC 版本"
						data={MC_VERSIONS}
						value={targetDraft.mcVersions}
						onChange={(val) => setTargetDraft({ ...targetDraft, mcVersions: val })}
						clearable
					/>
					<Text size="xs" c="dimmed">
						每个加载器与每个 MC 版本的组合都会加入列表，例如 Forge + 1.20.1/1.20 会生成两项。
					</Text>
					<Group justify="flex-end" mt="xs">
						<Button variant="default" onClick={() => setTargetOpen(false)}>
							取消
						</Button>
						<Button onClick={confirmTargets}>确定</Button>
					</Group>
				</Stack>
			</Modal>

			<Modal opened={editing !== null} onClose={() => setEditing(null)} title="编辑资料条目">
				{draft && (
					<Stack gap="sm">
						<TextInput
							label="名称"
							value={draft.name}
							onChange={(e) => setDraft({ ...draft, name: e.currentTarget.value })}
						/>
						<TextInput
							label="次要名称（英文）"
							placeholder="取自 en_us.json"
							value={draft.ename}
							onChange={(e) => setDraft({ ...draft, ename: e.currentTarget.value })}
						/>
						<TextInput
							label="注册名"
							placeholder="modid:path"
							value={draft.regname}
							onChange={(e) => setDraft({ ...draft, regname: e.currentTarget.value })}
						/>
						<Select
							label="资料分类"
							data={ENTRY_CATEGORIES}
							value={draft.category}
							onChange={(val) => setDraft({ ...draft, category: val ?? "物品/方块" })}
						/>
						<TextInput
							label="资料类型"
							value={draft.type}
							onChange={(e) => setDraft({ ...draft, type: e.currentTarget.value })}
						/>
						<Grid gutter="sm">
							<Grid.Col span={6}>
								<TextInput
									label="最大耐久"
									value={draft.damage}
									onChange={(e) => setDraft({ ...draft, damage: e.currentTarget.value })}
								/>
							</Grid.Col>
							<Grid.Col span={6}>
								<TextInput
									label="最大堆叠"
									value={draft.stack}
									onChange={(e) => setDraft({ ...draft, stack: e.currentTarget.value })}
								/>
							</Grid.Col>
						</Grid>
						<Group justify="flex-end" mt="xs">
							<Button variant="default" onClick={() => setEditing(null)}>
								取消
							</Button>
							<Button onClick={confirmEntry}>保存</Button>
						</Group>
					</Stack>
				)}
			</Modal>
		</Box>
	);
}
